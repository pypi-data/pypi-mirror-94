************
openapi-core
************

.. image:: https://img.shields.io/pypi/v/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core
.. image:: https://travis-ci.org/p1c2u/openapi-core.svg?branch=master
     :target: https://travis-ci.org/p1c2u/openapi-core
.. image:: https://img.shields.io/codecov/c/github/p1c2u/openapi-core/master.svg?style=flat
     :target: https://codecov.io/github/p1c2u/openapi-core?branch=master
.. image:: https://img.shields.io/pypi/pyversions/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core
.. image:: https://img.shields.io/pypi/format/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core
.. image:: https://img.shields.io/pypi/status/openapi-core.svg
     :target: https://pypi.python.org/pypi/openapi-core

About
#####

Openapi-core is a Python library that adds client-side and server-side support
for the `OpenAPI Specification v3.0.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md>`__.

Installation
############

Recommended way (via pip):

::

    $ pip install openapi-core

Alternatively you can download the code and install from the repository:

.. code-block:: bash

   $ pip install -e git+https://github.com/p1c2u/openapi-core.git#egg=openapi_core


Usage
#####

Firstly create your specification:

.. code-block:: python

   from openapi_core import create_spec

   spec = create_spec(spec_dict)

Request
*******

Now you can use it to validate requests

.. code-block:: python

   from openapi_core.validation.request.validators import RequestValidator

   validator = RequestValidator(spec)
   result = validator.validate(request)

   # raise errors if request invalid
   result.raise_for_errors()

   # get list of errors
   errors = result.errors

and unmarshal request data from validation result

.. code-block:: python

   # get parameters object with path, query, cookies and headers parameters
   validated_params = result.parameters
   # or specific parameters
   validated_path_params = result.parameters.path

   # get body
   validated_body = result.body

   # get security data
   validated_security = result.security

Request object should be instance of OpenAPIRequest class (See `Integrations`_).

Response
********

You can also validate responses

.. code-block:: python

   from openapi_core.validation.response.validators import ResponseValidator

   validator = ResponseValidator(spec)
   result = validator.validate(request, response)

   # raise errors if response invalid
   result.raise_for_errors()

   # get list of errors
   errors = result.errors

and unmarshal response data from validation result

.. code-block:: python

   # get headers
   validated_headers = result.headers

   # get data
   validated_data = result.data

Response object should be instance of OpenAPIResponse class (See `Integrations`_).

Security
********

openapi-core supports security for authentication and authorization process. Security data for security schemas are accessible from `security` attribute of `RequestValidationResult` object.

For given security specification:

.. code-block:: yaml

   security:
     - BasicAuth: []
     - ApiKeyAuth: []
   components:
     securitySchemes:
       BasicAuth:
         type: http
         scheme: basic
       ApiKeyAuth:
         type: apiKey
         in: header
         name: X-API-Key

you can access your security data the following:

.. code-block:: python

   result = validator.validate(request)

   # get basic auth decoded credentials
   result.security['BasicAuth']

   # get api key
   result.security['ApiKeyAuth']

Supported security types:

* http – for Basic and Bearer HTTP authentications schemes
* apiKey – for API keys and cookie authentication


Customizations
##############

Deserializers
*************

Pass custom defined media type deserializers dictionary with supported mimetypes as a key to `RequestValidator` or `ResponseValidator` constructor:

.. code-block:: python

   def protobuf_deserializer(message):
       feature = route_guide_pb2.Feature()
       feature.ParseFromString(message)
       return feature

   custom_media_type_deserializers = {
       'application/protobuf': protobuf_deserializer,
   }

   validator = ResponseValidator(
       spec, custom_media_type_deserializers=custom_media_type_deserializers)

   result = validator.validate(request, response)

Formats
*******

OpenAPI defines a ``format`` keyword that hints at how a value should be interpreted, e.g. a ``string`` with the type ``date`` should conform to the RFC 3339 date format.

Openapi-core comes with a set of built-in formatters, but it's also possible to add support for custom formatters for `RequestValidator` and `ResponseValidator`.

Here's how you could add support for a ``usdate`` format that handles dates of the form MM/DD/YYYY:

.. code-block:: python

    from datetime import datetime
    import re

    class USDateFormatter:
        def validate(self, value) -> bool:
            return bool(re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", value))

        def unmarshal(self, value):
            return datetime.strptime(value, "%m/%d/%y").date


   custom_formatters = {
       'usdate': USDateFormatter(),
   }

   validator = ResponseValidator(spec, custom_formatters=custom_formatters)

   result = validator.validate(request, response)

Integrations
############

Django
******

For Django 2.2 you can use DjangoOpenAPIRequest a Django request factory:

.. code-block:: python

   from openapi_core.validation.request.validators import RequestValidator
   from openapi_core.contrib.django import DjangoOpenAPIRequest

   openapi_request = DjangoOpenAPIRequest(django_request)
   validator = RequestValidator(spec)
   result = validator.validate(openapi_request)

You can use DjangoOpenAPIResponse as a Django response factory:

.. code-block:: python

   from openapi_core.validation.response.validators import ResponseValidator
   from openapi_core.contrib.django import DjangoOpenAPIResponse

   openapi_response = DjangoOpenAPIResponse(django_response)
   validator = ResponseValidator(spec)
   result = validator.validate(openapi_request, openapi_response)

Falcon
******

This section describes integration with `Falcon <https://falconframework.org>`__ web framework.

Middleware
==========

Falcon API can be integrated by `FalconOpenAPIMiddleware` middleware.

.. code-block:: python

   from openapi_core.contrib.falcon.middlewares import FalconOpenAPIMiddleware

   openapi_middleware = FalconOpenAPIMiddleware.from_spec(spec)
   api = falcon.API(middleware=[openapi_middleware])

Low level
=========

For Falcon you can use FalconOpenAPIRequest a Falcon request factory:

.. code-block:: python

   from openapi_core.validation.request.validators import RequestValidator
   from openapi_core.contrib.falcon import FalconOpenAPIRequestFactory

   openapi_request = FalconOpenAPIRequestFactory.create(falcon_request)
   validator = RequestValidator(spec)
   result = validator.validate(openapi_request)

You can use FalconOpenAPIResponse as a Falcon response factory:

.. code-block:: python

   from openapi_core.validation.response.validators import ResponseValidator
   from openapi_core.contrib.falcon import FalconOpenAPIResponseFactory

   openapi_response = FalconOpenAPIResponseFactory.create(falcon_response)
   validator = ResponseValidator(spec)
   result = validator.validate(openapi_request, openapi_response)

Flask
*****

Decorator
=========

Flask views can be integrated by `FlaskOpenAPIViewDecorator` decorator.

.. code-block:: python

   from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator

   openapi = FlaskOpenAPIViewDecorator.from_spec(spec)

   @app.route('/home')
   @openapi
   def home():
       pass

If you want to decorate class based view you can use the decorators attribute:

.. code-block:: python

   class MyView(View):
       decorators = [openapi]

View
====

As an alternative to the decorator-based integration, Flask method based views can be integrated by inheritance from `FlaskOpenAPIView` class.

.. code-block:: python

   from openapi_core.contrib.flask.views import FlaskOpenAPIView

   class MyView(FlaskOpenAPIView):
       pass

   app.add_url_rule('/home', view_func=MyView.as_view('home', spec))

Request parameters
==================

In Flask, all unmarshalled request data are provided as Flask request object's openapi.parameters attribute

.. code-block:: python

   from flask.globals import request

   @app.route('/browse/<id>/')
   @openapi
   def home():
       browse_id = request.openapi.parameters.path['id']
       page = request.openapi.parameters.query.get('page', 1)

Low level
=========

You can use FlaskOpenAPIRequest a Flask/Werkzeug request factory:

.. code-block:: python

   from openapi_core.validation.request.validators import RequestValidator
   from openapi_core.contrib.flask import FlaskOpenAPIRequest

   openapi_request = FlaskOpenAPIRequest(flask_request)
   validator = RequestValidator(spec)
   result = validator.validate(openapi_request)

You can use FlaskOpenAPIResponse as a Flask/Werkzeug response factory:

.. code-block:: python

   from openapi_core.validation.response.validators import ResponseValidator
   from openapi_core.contrib.flask import FlaskOpenAPIResponse

   openapi_response = FlaskOpenAPIResponse(flask_response)
   validator = ResponseValidator(spec)
   result = validator.validate(openapi_request, openapi_response)

Pyramid
*******

See `pyramid_openapi3  <https://github.com/niteoweb/pyramid_openapi3>`_ project.

Bottle
*******

See `bottle-openapi-3  <https://github.com/cope-systems/bottle-openapi-3>`_ project.


Requests
********

This section describes integration with `Requests <https://requests.readthedocs.io>`__ library.

Low level
=========

For Requests you can use RequestsOpenAPIRequest a Requests request factory:

.. code-block:: python

   from openapi_core.validation.request.validators import RequestValidator
   from openapi_core.contrib.requests import RequestsOpenAPIRequest

   openapi_request = RequestsOpenAPIRequest(requests_request)
   validator = RequestValidator(spec)
   result = validator.validate(openapi_request)

You can use RequestsOpenAPIResponse as a Requests response factory:

.. code-block:: python

   from openapi_core.validation.response.validators import ResponseValidator
   from openapi_core.contrib.requests import RequestsOpenAPIResponse

   openapi_response = RequestsOpenAPIResponse(requests_response)
   validator = ResponseValidator(spec)
   result = validator.validate(openapi_request, openapi_response)

Related projects
################
* `openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`__
* `openapi-schema-validator <https://github.com/p1c2u/openapi-schema-validator>`__
* `pyramid_openapi3 <https://github.com/niteoweb/pyramid_openapi3>`__
