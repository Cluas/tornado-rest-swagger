tornado-rest-swagger
===============

![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/Cluas/tornado-rest-swagger.svg)
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
Issues | https://github.com/Cluas/tornado-rest-swaggerr/issues
Python version | python2.7 and Python 3.4 and above
Swagger Language Specification | https://swagger.io/specification

Installation
----------------------

    pip install -U tornado-rest-swagger


What's tornado-rest-swagger
----------------------

tornado-swagger is a plugin for tornado server that allow to document APIs using Swagger show the Swagger-ui console.

![](https://github.com/Cluas/tornado-rest-swagger/blob/master/docs/wiki__swagger_single_endpoint.png)

```python
class PostsDetailsHandler(tornado.web.RequestHandler):
    def get(self, posts_id):
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
```


### Version 1.1.1

- First version released


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FCluas%2Ftornado-rest-swagger.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FCluas%2Ftornado-rest-swagger?ref=badge_shield)