from tornado_swagger.builders import extract_swagger_docs


class RegisterDict(dict):
    def register(self, item):
        doc = item.__doc__

        if doc is not None and "---" in doc:
            self[item.__name__] = extract_swagger_docs(doc)


class Components(object):
    def __init__(self):
        self.schemas = RegisterDict()
        self.parameters = RegisterDict()
        self.security_schemes = RegisterDict()
        self.request_bodies = RegisterDict()
        self.responses = RegisterDict()
        self.headers = RegisterDict()
        self.examples = RegisterDict()
        self.links = RegisterDict()
        self.callbacks = RegisterDict()

    def to_dict(self):
        return dict(
            schemas=self.schemas,
            parameters=self.parameters,
            securitySchemes=self.security_schemes,
            requestBodies=self.request_bodies,
            responses=self.responses,
            headers=self.headers,
            examples=self.examples,
            links=self.links,
            callbacks=self.callbacks,
        )


components = Components()
