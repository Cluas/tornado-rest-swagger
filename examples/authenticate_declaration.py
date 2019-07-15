import tornado.ioloop
import tornado.options
import tornado.web

from tornado_swagger.components import components
from tornado_swagger.setup import setup_swagger


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class ExampleHandler(BaseHandler):
    def post(self):
        """
        Description end-point

        ---
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
        self.write({})


@components.security_schemes.register
class JWTToken(object):
    """
    ---
    type: http
    scheme: bearer
    bearerFormat: JWT
    """


class Application(tornado.web.Application):
    _routes = [tornado.web.url(r"/api/example", ExampleHandler, name="example")]

    def __init__(self):
        settings = {"debug": True}

        setup_swagger(self._routes)
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":
    tornado.options.define("port", default="8080", help="Port to listen on")
    tornado.options.parse_command_line()

    app = Application()
    app.listen(port=8080)

    tornado.ioloop.IOLoop.current().start()
