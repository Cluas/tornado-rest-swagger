import sys

import tornado.web

from tornado_swagger.builders import build_doc_from_func_doc
from tornado_swagger.builders import extract_parameters_names
from tornado_swagger.builders import format_handler_path
from tornado_swagger.builders import extract_swagger_docs
from tornado_swagger.builders import generate_doc_from_endpoints
from tornado_swagger.builders import SWAGGER_DOC_SEPARATOR

INVALID_ENDPOINT_DOC = SWAGGER_DOC_SEPARATOR + """
tag"""
ENDPOINT_DOC = SWAGGER_DOC_SEPARATOR + """
tags:
  - Example
summary: Create user
description: This can only be done by the logged in user.
operationId: examples.api.api.createUser
requestBody:
    description: Created user object
    required: false
    content:
        application/json:
        schema:
          type: object
          properties:
            id:
              type: integer
              format: int64
            username:
              type:
                - "string"
                - "null"
            firstName:
              type: string
            lastName:
              type: string
            email:
              type: string
            password:
              type: string
            phone:
              type: string
            userStatus:
              type: integer
              format: int32
              description: User Status
responses:
"201":
  description: successful operation
"""


def test_extract_swagger_docs():
    docs = extract_swagger_docs(ENDPOINT_DOC)
    assert 'Invalid Swagger' not in docs['tags']


def test_invalid_extract_swagger_docs():
    docs = extract_swagger_docs(INVALID_ENDPOINT_DOC)
    assert 'Invalid Swagger' in docs['tags']


class ExampleHandler(tornado.web.RequestHandler):
    def get(self):
        pass


def test_build_doc_from_func_doc():
    if sys.version >= "3":
        ExampleHandler.get.__doc__ = ENDPOINT_DOC
    else:
        ExampleHandler.get.__func__.__doc__ = ENDPOINT_DOC
    docs = build_doc_from_func_doc(ExampleHandler)
    assert 'Invalid Swagger' not in docs['get']['tags']


def test_generate_doc_from_each_end_point():
    if sys.version >= "3":
        ExampleHandler.get.__doc__ = ENDPOINT_DOC
    else:
        ExampleHandler.get.__func__.__doc__ = ENDPOINT_DOC
    routes = [
        tornado.web.url(r'/api/example', ExampleHandler, name='example'),
    ]

    docs = generate_doc_from_endpoints(
        routes,
        servers=None,
        api_base_url='/',
        description='',
        api_version='',
        title='',
        contact=None,
        external_docs=None,
        security=None
    )
    assert docs


def test_extract_parameters_names_empty_parameter():
    class HandlerWithEmptyParameter(tornado.web.RequestHandler):
        def get(self):
            pass

    parameters = extract_parameters_names(HandlerWithEmptyParameter, 0)
    assert parameters == []


def test_extract_parameters_names_signle_parameter():
    class HandlerWithSingleParameter(tornado.web.RequestHandler):
        def get(self, posts_id):
            pass

    parameters = extract_parameters_names(HandlerWithSingleParameter, 1)
    assert parameters == ['posts_id']


def test_extract_parameters_names_multiple():
    class HandlerWithMultipleParameter(tornado.web.RequestHandler):
        def get(self, posts_id, post_id2, post_id3):
            pass

    parameters = extract_parameters_names(HandlerWithMultipleParameter, 3)
    assert parameters == ['posts_id', 'post_id2', 'post_id3']


def test__format_handler_path():
    class HandlerWithMultipleParameter(tornado.web.RequestHandler):
        def get(self, posts_id, post_id2, post_id3):
            pass
    url = tornado.web.url(r'/api/(\w+)/(\w+)/(\w+)', HandlerWithMultipleParameter)
    route_path = format_handler_path(HandlerWithMultipleParameter, url.regex.pattern, url.regex.groups)
    assert route_path == '/api/{posts_id}/{post_id2}/{post_id3}'
