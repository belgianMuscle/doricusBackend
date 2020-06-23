# Doricus - Backend

## Introduction
Welcome to the Doricus Backend. Doricus is a Construction Management Platform which is meant to help Architects, Builders and Customers communicate and track progress. More information about Doricus can be found at: URL to come. 

This backend has been developed with Python using the Flask framework. We are currently using a Postgres database to host all the data necessary for the app to work. 
Additionally we are using Auth0 for authentication and role based permissions.

This backend is meant to be accessible as an API for the frontend. CORS will only be available to the appropriate resources.

## How-to install
The backend has been developed to be hosted mainly on a Heroku instance. Potentially we will prepare the package to be easy to deploy as a Docker container on a AWS Kubernetes cluster.

To run locally you can first start with

```
$ pip install -r requirements.txt
```
The first step will be to setup your database using

```
$ createdb Doricus
```

If you are not running a local postgres server or are renaming the database name to something else you will need the following environment variables to be set

```
$ export DB_NAME={your db name} (this one is only necessary for local runs, in Heroku we are already running a live instance)
$ export DATABASE_URL={your postgres path}
```

Once that is setup you can proceed with creating your database by running

```
$ python manage.py db upgrade
```

Additionally we need to set the Authorization variables

```
$ export AUTH_DOMAIN={your auth0 domain}
$ export AUTH_AUDIENCE={your audience, default value is Doricus}
```

Now we are ready to run the backend locally

```
$ export FLASK_APP=app.py
$ flask run
```

## API Documentation

### Members
#### GET '/members'
```
- Fetches the current member's information based on the authenticated user
- Request arguments: None
- Request headers: Authorization token
- Returns an object with a success field and a field containing the member data
- If the request gets an invalid authorization header, the result will be an empty member in the response and a False success value.
- If the member does not align with the appropriate Authentication user id, the request will return a HTTP 403 error
{ 
    'success':True,
    'member':{}
}
```

#### POST '/members'
```
- This operation creates a new member record for the supplied authorization header
- Validations: 
    - Check if request data is provided
    - Check if Authorization id is provided
- Request arguments: None
- Request headers: Authorization token, json body with member data
- Request data:
{ 
    'member':{}
}
- Returns the created member object
{ 
    'success':True,
    'member':{}
}
```

#### PATCH '/members/<member_id>'
```
- This operation updates an existing member
- Validations:
    - Check if member with request argument exists
    - Check if request data is provided
    - Check if Authorization id is provided
- Request arguments: member id
- Request headers: Authorization token, json body with member data
- Request data:
{ 
    'member':{}
}
- Returns the created member object
{ 
    'success':True,
    'member':{}
}
```

### Projects
#### GET '/projects'
```

```


### Error Codes

- 404: Resource not found
- 405: Method not allowed
- 422: Resrouce cannot be processed
- 400: Bad request
- 500: Request not allowed

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```