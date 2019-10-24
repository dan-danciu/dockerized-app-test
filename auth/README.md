# AUTH container module

## Purpose

The auth module receives a username and password in formdata and then returns a JWT token (that only contains a reference to the user through a login ID or something) and a refresh token.

The JWT token is used by the client on each HTTP request to the backend apis.
The JWT token is short lived.

The refresh token is long lived and is used together with an expired JWT token to automatically generate a new valid JWT token for as long as the client holds both a JWT token and a refresh token.