import datetime
from typing import TYPE_CHECKING

from typing import List

import sqlalchemy as sa  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy_utils import JSONType  # type: ignore

from aws_session_recorder.lib.helpers import AlwaysDoNothing
from aws_session_recorder.lib.schema.base import Base, TimeStamp

if TYPE_CHECKING:
    from mypy_boto3_iam import type_defs as t  # type: ignore
else:
    t = AlwaysDoNothing()
    client = AlwaysDoNothing()

# policy_attachments = sa.Table('policy_attachments', Base.metadata,
#                               sa.Column('identity_PolicyArn', sa.Integer, sa.ForeignKey('identity.id')),
#                               sa.Column('policy_PolicyArn', sa.Integer, sa.ForeignKey('policy.id')),
#                               )


class UserPolicyAttachments(Base):
    __tablename__ = "user_policy_attachments"

    def __init__(self, resp):
        super().__init__(**resp)

    UserName = sa.Column('UserName', sa.String, sa.ForeignKey('user.UserName'), primary_key=True)
    PolicyArn = sa.Column('PolicyArn', sa.String, sa.ForeignKey('policy.Arn'), primary_key=True)
    PolicyName = sa.Column('PolicyName', sa.String)

    user = relationship('User', back_populates='attached_policies')
    policy = relationship('Policy', back_populates='attached_to_users')


class RolePolicyAttachments(Base):
    __tablename__ = "role_policy_attachments"

    def __init__(self, resp):
        super().__init__(**resp)

    RoleName = sa.Column('RoleName', sa.String, sa.ForeignKey('role.RoleName'), primary_key=True)
    PolicyArn = sa.Column('PolicyArn', sa.String, sa.ForeignKey('policy.Arn'), primary_key=True)
    PolicyName = sa.Column('PolicyName', sa.String)

    role = relationship('Role', back_populates='attached_policies')
    policy = relationship('Policy', back_populates='attached_to_roles')


class GroupPolicyAttachments(Base):
    __tablename__ = "group_policy_attachments"

    def __init__(self, resp):
        super().__init__(**resp)

    GroupName = sa.Column('GroupName', sa.String, sa.ForeignKey('group.GroupName'), primary_key=True)
    PolicyArn = sa.Column('PolicyArn', sa.String, sa.ForeignKey('policy.Arn'), primary_key=True)
    PolicyName = sa.Column('PolicyName', sa.String)

    group = relationship('Group', back_populates='attached_policies')
    policy = relationship('Policy', back_populates='attached_to_groups')


class Policy(Base):
    __tablename__ = "policy"

    def __init__(self, resp):
        super().__init__(**resp)

    id = sa.Column(sa.Integer, unique=True, autoincrement=True)
    PolicyName = sa.Column(sa.String)
    PolicyId = sa.Column(sa.String)
    Arn = sa.Column(sa.String, primary_key=True)
    Path = sa.Column(sa.String)
    DefaultVersionId = sa.Column(sa.String)
    AttachmentCount = sa.Column(sa.String)
    PermissionsBoundaryUsageCount = sa.Column(sa.Integer)
    IsAttachable = sa.Column(sa.Boolean)
    Description = sa.Column(sa.String)
    CreateDate: datetime.datetime = sa.Column(TimeStamp)
    UpdateDate: datetime.datetime = sa.Column(TimeStamp)

    attached_to_users = relationship("UserPolicyAttachments", back_populates='policy')
    attached_to_roles = relationship("RolePolicyAttachments", back_populates='policy')
    attached_to_groups = relationship("GroupPolicyAttachments", back_populates='policy')

    versions: 'List[PolicyVersion]' = relationship("PolicyVersion", back_populates="policy")


class PolicyVersion(Base):
    __tablename__ = "policy_version"

    def __init__(self, resp: 't.PolicyVersionTypeDef'):
        print(f'response {resp}')
        super().__init__(**resp)

    VersionId: str = sa.Column(sa.String, primary_key=True)
    PolicyVersion: str = sa.Column(sa.String)
    Document: dict = sa.Column(JSONType)
    IsDefaultVersion: bool = sa.Column(sa.Boolean)
    CreateDate: datetime.datetime = sa.Column(TimeStamp)

    policy_id: int = sa.Column(sa.Integer, sa.ForeignKey('policy.id'))
    policy = relationship("Policy", back_populates="versions")
