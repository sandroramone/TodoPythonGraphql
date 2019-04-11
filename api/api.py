from os import path
from flask import Flask
from flask_graphql import GraphQLView

from models.base import db
from v1_graphql.schema import schema


def create_api(mode='development'):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)),
        '{}_instance'.format(mode)
    )

    app = Flask(
        __name__,
        instance_path=instance_path
    )

    app.config['JWT_SECRET_KEY'] = 'is secret'
    app.config.from_object('configdb')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    app.add_url_rule(
        '/v1/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

    db.init_app(app=app)
    return app
