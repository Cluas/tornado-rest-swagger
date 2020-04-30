import collections
import inspect
import os
import re
import sys

import yaml
from jinja2 import BaseLoader
from jinja2 import Environment
import tornado.web

if sys.version >= "3":
    from inspect import getfullargspec
else:

    class getfullargspec(object):
        """A quick and dirty replacement for getfullargspec for Python 2.X"""

        def __init__(self, f):
            self.args, self.varargs, self.varkw, self.defaults = inspect.getargspec(f)
            self.kwonlyargs = []
            self.kwonlydefaults = None

        def __iter__(self):
            yield self.args
            yield self.varargs
            yield self.varkw
            yield self.defaults


SWAGGER_TEMPLATE = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "swagger.yaml"))
SWAGGER_DOC_SEPARATOR = "---"


def _extract_swagger_definition(endpoint_doc):
    endpoint_doc = endpoint_doc.splitlines()

    # Find Swagger start point in doc
    for i, doc_line in enumerate(endpoint_doc):
        if SWAGGER_DOC_SEPARATOR in doc_line:
            end_point_swagger_start = i + 1
            endpoint_doc = endpoint_doc[end_point_swagger_start:]
            break
    return "\n".join(endpoint_doc)


def extract_swagger_docs(endpoint_doc):
    endpoint_doc = _extract_swagger_definition(endpoint_doc)

    # Build JSON YAML Obj
    try:
        end_point_swagger_doc = yaml.safe_load(endpoint_doc)
        if not isinstance(end_point_swagger_doc, dict):
            raise yaml.YAMLError()
    except yaml.YAMLError as e:
        end_point_swagger_doc = {
            "description": "Swagger document could not be loaded from docstring, error details : %s" % e,
            "tags": ["Invalid Swagger"],
        }
    return end_point_swagger_doc


def build_doc_from_func_doc(handler):
    out = {}

    for method in handler.SUPPORTED_METHODS:
        method = method.lower()
        doc = getattr(handler, method).__doc__

        if doc is not None and "---" in doc:
            out.update({method: extract_swagger_docs(doc)})

    return out


def try_extract_docs(method_handler):
    try:
        return getfullargspec(method_handler).args[1:]
    except TypeError:  # unsupported callable
        if hasattr(method_handler, "__wrapped__"):
            return try_extract_docs(method_handler.__wrapped__)
        else:
            return []


def extract_parameters_names(handler, parameters_count):
    if parameters_count == 0:
        return []

    parameters = ["{?}" for _ in range(parameters_count)]

    for method in handler.SUPPORTED_METHODS:
        method_handler = getattr(handler, method.lower())
        args = try_extract_docs(method_handler)

        if len(args) > 0:
            for i, arg in enumerate(args):
                if set(arg) != {"_"}:
                    parameters[i] = arg

    return parameters


def format_handler_path(target, route_pattern, groups):
    brackets_regex = re.compile(r"\(.*?\)")
    parameters = extract_parameters_names(target, groups)

    for i, entity in enumerate(brackets_regex.findall(route_pattern)):
        route_pattern = route_pattern.replace(entity, "{%s}" % parameters[i], 1)

    return route_pattern[:-1]


def nesteddict2yaml(d, indent=10, result=""):
    for key, value in d.items():
        result += " " * indent + str(key) + ":"
        if isinstance(value, dict):
            result = nesteddict2yaml(value, indent + 2, result + "\n")
        else:
            result += " " + str(value) + "\n"
    return result


def generate_doc_from_endpoints(routes, servers, description, api_version, title, contact, external_docs, security):
    from tornado_swagger.components import components

    # Clean description
    _start_desc = 0
    for i, word in enumerate(description):
        if word != "\n":
            _start_desc = i
            break
    cleaned_description = "    ".join(description[_start_desc:].splitlines())

    # Load base Swagger template
    jinja2_env = Environment(loader=BaseLoader())
    jinja2_env.filters["nesteddict2yaml"] = nesteddict2yaml

    with open(SWAGGER_TEMPLATE, "r") as f:
        swagger_base = jinja2_env.from_string(f.read()).render(
            description=cleaned_description,
            version=api_version,
            title=title,
            contact=contact,
            servers=servers,
            external_docs=external_docs,
        )

    # The Swagger OBJ
    swagger = yaml.safe_load(swagger_base)
    swagger["paths"] = collections.defaultdict(dict)
    swagger["security"] = security
    swagger["components"] = components.to_dict()
    swagger["servers"] = servers

    for route in routes:
        if isinstance(route, tuple):
            route = tornado.web.url(*route)
        if tornado.version >= "5.0":
            target = route.target
        else:
            target = route.handler_class
        swagger["paths"][format_handler_path(target, route.regex.pattern, route.regex.groups)].update(
            build_doc_from_func_doc(target)
        )

    return swagger
