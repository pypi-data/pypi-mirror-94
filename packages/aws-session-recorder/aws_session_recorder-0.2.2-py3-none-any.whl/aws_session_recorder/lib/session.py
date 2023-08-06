"""Main module."""
import os

import boto3  # type: ignore
import botocore.client  # type: ignore
import botocore.model  # type: ignore
import botocore.awsrequest  # type: ignore
import sqlalchemy  # type: ignore
import sqlalchemy.orm  # type: ignore
import sqlalchemy.ext.declarative  # type: ignore

from aws_session_recorder.lib.schema.functions import ApiCallMap
from aws_session_recorder.lib.schema.base import Base


class Session(boto3.session.Session):
    db: sqlalchemy.orm.Session
    Base: sqlalchemy.ext.declarative.DeclarativeMeta

    def __init__(self, connection_string: str = f"sqlite:///{os.path.join(os.getcwd(), 'sqlite.db')}", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup(connection_string=connection_string)

    def setup(self, connection_string: str):
        engine = sqlalchemy.create_engine(connection_string, echo=False)
        Base.metadata.create_all(engine)
        self.db = sqlalchemy.orm.Session(engine)

    def client(self, *args, **kwargs):
        client: botocore.client.BaseClient = super().client(*args, **kwargs)
        client.meta.events.register('provide-client-params.iam.*', self.record_request)
        client.meta.events.register('after-call.iam.*', self.record_response)
        return client

    def record_request(
        self,
        params: dict,
        model: botocore.model.OperationModel,
        context: dict,
        event_name: str,
        *args, **kwargs
    ):
        context['request_params'] = params

    def record_response(self,
                        http_response: botocore.awsrequest.AWSResponse,
                        parsed: dict,
                        model: botocore.model.OperationModel,
                        context: dict,
                        event_name: str,
                        *args, **kwargs):

        try:
            f = ApiCallMap[model.name]
        except KeyError:
            print("Schema not implemented for {}".format(model.name))
            return

        request_params = context['request_params']
        parsed_resp = parsed
        row = f(request_params, parsed_resp)  # type: ignore[arg-type]
        if hasattr(row, '__next__'):
            for r in row:
                self.db.merge(r)
        else:
            self.db.merge(row)

        self.db.commit()
        self.db.flush()
