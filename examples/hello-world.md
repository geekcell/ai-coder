A microservice that returns a greeting to the user.

The microservice has a REST API which exposes exactly one endpoint called "/greeting" that returns a JSON object with a key "greeting" and a value of "Hello, world!". Optionally, the endpoint can accept a query parameter called "name" and return a greeting with the name included.

First example:

Request:
GET /greeting?name=John

Response:
{
    "greeting": "Hello, John!"
}

Second example:

Request:
GET /greeting

Response:
{
    "greeting": "Hello, world!"
}

You must also include include an OpenAPI specification for the REST API.
