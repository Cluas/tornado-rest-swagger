import json
import os

import tornado.web

from tornado_swagger.builders import generate_doc_from_endpoints
from tornado_swagger.handlers import SwaggerHomeHandler

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger_ui"))


def export_swagger(
    routes,
    servers=None,
    description="Swagger API definition",
    api_version="1.0.0",
    title="Swagger API",
    contact="",
    external_docs=None,
    security=None,
):
    return generate_doc_from_endpoints(
        routes,
        servers=servers,
        description=description,
        api_version=api_version,
        title=title,
        contact=contact,
        external_docs=external_docs,
        security=security,
    )


def setup_swagger(
    routes,
    swagger_url="/docs",
    servers=None,
    description="Swagger API definition",
    api_version="1.0.0",
    title="Swagger API",
    contact="",
    external_docs=None,
    security=None,
):
    swagger_schema = generate_doc_from_endpoints(
        routes,
        servers=servers,
        description=description,
        api_version=api_version,
        title=title,
        contact=contact,
        external_docs=external_docs,
        security=security,
    )

    _swagger_url = "/{}".format(swagger_url) if not swagger_url.startswith("/") else swagger_url
    _base_swagger_url = _swagger_url.rstrip("/")

    routes += [
        tornado.web.url(_swagger_url, SwaggerHomeHandler),
        tornado.web.url("{}/".format(_base_swagger_url), SwaggerHomeHandler),
    ]

    with open(os.path.join(STATIC_PATH, "ui.jinja2"), "r") as f:
        SwaggerHomeHandler.SWAGGER_HOME_TEMPLATE = f.read().replace("{{ SWAGGER_SCHEMA }}", json.dumps(swagger_schema))
