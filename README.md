# dockerized-app-test

# Run it in development
```
docker-compose -f dev.docker-compose.yml up --build
```

# Components
## nginx

There are two Dockerfiles. 
One is for development which does not include the frontend, instead it proxies to the frontend dev server.
One should eventually be used for building for production. This one will serve the frontend and proxy to the backend as well.

## frontend

This container only exists in development because it is used to hot reload changes as they happen. This makes for a nice development experience.
The frontend is created with vuejs.
In development it runs with `npm run serve`.
In production it is built and the dist folder is served from the nginx server.

## api

The api is python fastapi.
It is capable of many nice things.
In production the image should be built from Dockerfile.
In development the dev.Dockerfile shall be used.
The difference is that in production it runs off of gunicorn based on it's configurations. In dev it runs on uvicorn with hot reload. This makes for a good development experience as changes are reflected immediately.

## mongo

This is the database. Nothing fancy, should be better secured at some point.

## mongo-express

Allows us to look directly into the database by using a nice GUI.
Should not be needed in production.

