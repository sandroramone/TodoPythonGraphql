import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


from models.database import db, TodoModel
from utils import clear_input


class Todo(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel


class Todos(graphene.ObjectType):
    todos = graphene.List(of_type=Todo)
    total_count = graphene.Int()

    def __init__(self, info, **kwargs):
        self.info = info
        self.kwargs = kwargs
        self.filters = []
        self.query = Todo.get_query(info)

        for key in kwargs:
            if type(kwargs.get(key)) == str:
                self.filters.append(
                    TodoModel.__dict__[key].like(
                        '%{}%'.format(kwargs.get(key))
                    )
                )
            elif key != 'limit' and key != 'offset':
                self.filters.append(
                    TodoModel.__dict__[key].is_(kwargs.get(key))
                )

    def resolve_total_count(self, info, **kwargs):
        return self.query.filter(*self.filters).count()

    def resolve_todos(self, info, **kwargs):
        offset = self.kwargs.pop('offset', 0)
        limit = self.kwargs.pop('limit', 10)
        return self.query.filter(*self.filters).offset(offset).limit(limit)


class CreateTodo(graphene.Mutation):
    todo = graphene.Field(lambda: Todo)

    class Arguments:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        parent = graphene.ID(required=False)

    def mutate(self, info, **kwargs):
        todo = None
        input = clear_input(kwargs)

        if 'id' in input:
            ident = input['id']
            del input['id']

            todo = db.session.query(TodoModel).filter_by(id=ident)
            todo.update(input)
            todo = db.session.query(TodoModel).filter_by(id=ident).first()
        else:
            todo = TodoModel(**input)
            db.session.add(todo)
        
        db.session.commit()

        return CreateTodo(todo=todo)