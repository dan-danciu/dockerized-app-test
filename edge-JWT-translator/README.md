# JWT translator that lives on the edge

## This is a briliant idea until proven otherwise

Purpose of this module is to take incomming JWT tokens that contain only reference to a login id and translate those into JWT tokens that contain user data, passing those along to the other service modules.

This can be done at nginx level.

[StackOverflow](https://stackoverflow.com/questions/32778839/how-do-i-make-web-service-calls-within-nginx)
[Nginx Documentation](https://www.nginx.com/blog/validating-oauth-2-0-access-tokens-nginx/)
[Nginx Example](https://github.com/nginxinc/NGINX-Demos/blob/master/oauth2-token-introspection-oss/frontend.conf)

Idea is this:

Proxy receives request from client whisch is destined for the backend api. 

It contains a Reference JWT so there is no user data leaking out to the internet in any way.

Nginx takes this request, sends it first to another service. This service validates the JWT, grabs real user data like name, email, roles etc. from the database. Then it creates a JWT that contains all this data (valid token).

This comes back to the nginx which adds this response to the original request and proxies it along the way to its intended destination.

Each container module should be able to validate JWT on it's own so when receiving this JWT all services will know if it is valid or not and teh best part is, they will not have to go read from the database to get the current user identity becaus eit is already included!

And that is not all. Nginx can cache the tokens and the response from the translator. So if a user makes 100 requests in 5 minutes the validation will connect to the database only once and the backend services will still have the user data at the ready without actually having to do the work.

This will be awesome. - Probably