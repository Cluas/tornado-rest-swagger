tornado-rest-swagger
===============

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FCluas%2Ftornado-rest-swagger.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FCluas%2Ftornado-rest-swagger?ref=badge_shield)
![GitHub](https://img.shields.io/github/license/Cluas/tornado-rest-swagger.svg)


| PyPI                                        |
|----------------------------------------------|
| [![PyPI][pypi_image]][pypi_link] |


[pypi_link]: https://pypi.org/project/tornado-rest-swagger/
[pypi_image]: https://img.shields.io/pypi/v/tornado-rest-swagger.svg





| Linux                                        | Windows                                      |
|----------------------------------------------|----------------------------------------------|
| [![TravisCI][travisci_image]][travisci_link] | [![AppVeyor][appveyor_image]][appveyor_link] |

[travisci_link]: https://travis-ci.org/Cluas/tornado-rest-swagger
[travisci_image]: https://travis-ci.org/Cluas/tornado-rest-swagger.svg?branch=master

[appveyor_link]: https://ci.appveyor.com/project/Cluas/tornado-rest-swagger/branch/master
[appveyor_image]: https://ci.appveyor.com/api/projects/status/kp5w5tdi3ae0mpas?svg=true

*tornado-rest-swagger: Swagger API Documentation builder for tornado server. Inspired by [aiohttp-swagger](https://github.com/cr0hn/aiohttp-swagger) package (based on this package sources).*

Documentation |  https://github.com/Cluas/tornado-rest-swagger/wiki
------------- | -------------------------------------------------
Code | https://github.com/Cluas/tornado-rest-swagger
Issues | https://github.com/Cluas/tornado-rest-swagger/issues
Python version | python2.7 and Python 3.4 and above
Swagger Language Specification | https://swagger.io/specification

Installation
----------------------

    pip install -U tornado-rest-swagger


What's tornado-rest-swagger
----------------------

tornado-rest-swagger is a plugin for tornado server that allow to document APIs using Swagger show the Swagger-ui console.

![](https://github.com/Cluas/tornado-rest-swagger/blob/master/docs/wiki__swagger_single_endpoint.png)

Example
----------------------
```python
import tornado.ioloop
import tornado.options
import tornado.web

from tornado_swagger.components import components
from tornado_swagger.setup import setup_swagger


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class PostsHandler(BaseHandler):
    def get(self):
        """
        ---
        tags:
          - Posts
        summary: List posts
        description: List all posts in feed
        operationId: getPost
        responses:
            '200':
              description: A list of users
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ArrayOfPostModel'
                application/xml:
                  schema:
                    $ref: '#/components/schemas/ArrayOfPostModel'
                text/plain:
                  schema:
                    type: string
        """

    def post(self):
        """
        ---
        tags:
          - Posts
        summary: Add a new Post to the blog
        operationId: addPost
        requestBody:
          description: Post object that needs to be added to the blog
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostModel'
            application/xml:
              schema:
                $ref: '#/components/schemas/PostModel'
          required: true
        responses:
          '405':
            description: Invalid input
            content: {}
        security:
          - petstore_auth:
              - 'write:pets'
              - 'read:pets'
        """


class PostsDetailsHandler(BaseHandler):
    def get(self, posts_id):
        """
        ---
        tags:
          - Posts
        summary: Find Post by ID
        description: Returns a single post
        operationId: getPostById
        parameters:
          - name: post_id
            in: path
            description: ID of post to return
            required: true
            schema:
              type: integer
              format: int64
        responses:
          '200':
            description: successful operation
            content:
              application/xml:
                schema:
                  $ref: '#/components/schemas/PostModel'
              application/json:
                schema:
                  $ref: '#/components/schemas/PostModel'
          '400':
            description: Invalid ID supplied
            content: {}
          '404':
            description: Pet not found
            content: {}
        security:
          - api_key: []
        """

    def patch(self, posts_id):
        """
        ---
        tags:
          - Posts
        summary: Find Post by ID
        description: Returns a single post
        operationId: getPostById
        parameters:
          - name: post_id
            in: path
            description: ID of post to return
            required: true
            schema:
              type: integer
              format: int64
        requestBody:
          description: Post object that needs to be added to the blog
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostModel'
            application/xml:
              schema:
                $ref: '#/components/schemas/PostModel'
          required: true
        responses:
          '400':
            description: Invalid ID supplied
            content: {}
          '404':
            description: Pet not found
            content: {}
        security:
          - api_key: []
        """

    def delete(self, posts_id):
        """
        ---
        tags:
          - Posts
        summary: Delete Post by ID
        description: Returns a single post
        operationId: getPostById
        parameters:
          - name: post_id
            in: path
            description: ID of post to return
            required: true
            schema:
              type: integer
              format: int64
        responses:
          '200':
            description: successful operation
            content:
              application/json:
                schema:
                  type: object
                  description: Post model representation
                  properties:
                    id:
                      type: integer
                      format: int64
                    title:
                      type: string
                    text:
                      type: string
                    is_visible:
                      type: boolean
                      default: true
          '400':
            description: Invalid ID supplied
            content: {}
          '404':
            description: Pet not found
            content: {}
        """


@components.schemas.register
class PostModel(object):
    """
    ---
    type: object
    description: Post model representation
    properties:
        id:
            type: integer
            format: int64
        title:
            type: string
        text:
            type: string
        is_visible:
            type: boolean
            default: true
    """


@components.schemas.register
class ArrayOfPostModel(object):
    """
    ---
    type: array
    description: Array of Post model representation
    items:
        $ref: '#/components/schemas/PostModel'
    """


@components.security_schemes.register
class JWTToken(object):
    """
    ---
    type: http
    scheme: bearer
    bearerFormat: JWT
    """


class Application(tornado.web.Application):
    _routes = [tornado.web.url(r"/api/posts", PostsHandler), tornado.web.url(r"/api/posts/(\w+)", PostsDetailsHandler)]

    def __init__(self):
        settings = {"debug": True}

        setup_swagger(
            self._routes,
            swagger_url="/doc",
            description="",
            api_version="1.0.0",
            title="Journal API",
            contact=dict(name="test", email="test@domain.com", url="https://www.cluas.me"),
        )
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":
    tornado.options.define("port", default="8080", help="Port to listen on")
    tornado.options.parse_command_line()

    app = Application()
    app.listen(port=8080)

    tornado.ioloop.IOLoop.current().start()


```

### Version 1.1.3

- Fully support OpenAPI3.0

### Version 1.1.2

- Support OpenAPI 3.0 Authentication

### Version 1.1.1

- First version released


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FCluas%2Ftornado-rest-swagger.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FCluas%2Ftornado-rest-swagger?ref=badge_shield)
