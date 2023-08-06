from typing import Optional, TypedDict
from flask import g
from strawberry.flask.views import GraphQLView


class UserPayload(TypedDict):
    id: int
    username: str
    email: str


class MyContext(TypedDict):
    current_user: Optional[UserPayload]


class MyGraphQLView(GraphQLView):
    def get_context(self) -> MyContext:
        payload: Optional[UserPayload] = g.current_user

        return {'current_user': payload}
