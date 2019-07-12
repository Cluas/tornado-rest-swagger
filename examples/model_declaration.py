import tornado.ioloop
import tornado.options
import tornado.web

from tornado_swagger.model import register_swagger_model
from tornado_swagger.setup import setup_swagger


class PostsHandler(tornado.web.RequestHandler):
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
          description: successful operation
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PostModel'
            '404':
              description: Not Found
              content: {}
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


class PostsDetailsHandler(tornado.web.RequestHandler):
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
        """


@register_swagger_model
class PostModel:
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


class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(r'/api/posts', PostsHandler),
        tornado.web.url(r'/api/posts/(\w+)', PostsDetailsHandler),
    ]

    def __init__(self):
        settings = {
            'debug': True
        }

        setup_swagger(self._routes,
                      swagger_url='/doc',
                      api_base_url='/',
                      description='',
                      api_version='1.0.0',
                      title='Journal API',
                      contact='name@domain',
                      schemes=['https'],
                      security_definitions={
                          'ApiKeyAuth': {
                              'type': 'apiKey',
                              'in': 'header',
                              'name': 'X-API-Key'
                          }
                      })
        super(Application, self).__init__(self._routes, **settings)


if __name__ == '__main__':
    tornado.options.define('port', default='8080', help='Port to listen on')
    tornado.options.parse_command_line()

    app = Application()
    app.listen(port=8080)

    tornado.ioloop.IOLoop.current().start()
