import graphql
import graphene
from graphene import relay

from v1_graphql.todo import (
    Todo,
    Todos,
    CreateTodo
)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    todo = graphene.Field(Todo, id=graphene.Int())
    todos = graphene.Field(
        Todos,
        limit=graphene.Int(),
        offset=graphene.Int()
    )

    def resolve_todo(self, context, **kwargs):
        return Todo.get_node(context, kwargs.get('id'))
    
    def resolve_todos(self, context, **kwargs):
        return Todos(info=context, **kwargs)

class Mutation(graphene.ObjectType):
    createTodo = CreateTodo.Field()

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        Todo,
        Todos
    ]
)
