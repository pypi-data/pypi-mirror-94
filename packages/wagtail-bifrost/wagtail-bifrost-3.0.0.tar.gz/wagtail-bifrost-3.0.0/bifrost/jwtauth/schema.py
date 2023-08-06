import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphql import GraphQLError


# Create your registration related graphql schemes here.


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):

    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user

        if user.is_superuser:
            raise GraphQLError("Something went wrong")

        return cls(user=info.context.user)


class ObtainPrivilegedJSONWebToken(graphene.Mutation):

    token = graphene.String()
    payload = GenericScalar(required=True)
    refresh_expires_in = graphene.Int(required=True)

    class Arguments:
        token = graphene.String(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update(
            {
                get_user_model().USERNAME_FIELD: graphene.String(required=True),
                "password": graphene.String(required=True),
            }
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @graphql_jwt.decorators.staff_member_required
    @graphql_jwt.decorators.token_auth
    def mutate(cls, root, info, **kwargs):
        return ObtainPrivilegedJSONWebToken()

    @classmethod
    def resolve(cls, root, info, **kwargs):
        cls()
