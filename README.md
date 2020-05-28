# Doricus - Backend

## Introduction
Welcome to the Doricus Backend. Doricus is a Construction Management Platform which is meant to help Architects, Builders and Customers communicate and track progress. More information about Doricus can be found at: URL to come. 

This backend has been developed with Python using the Flask framework. We are currently using a Postgres database to host all the data necessary for the app to work. 
Additionally we are using Auth0 for authentication and role based permissions.

This backend is meant to be accessible as an API for the frontend. CORS will only be available to the appropriate resources.

## How-to install
The backend has been developed to be hosted mainly on a Heroku instance. Potentially we will prepare the package to be easy to deploy as a Docker container on a AWS Kubernetes cluster.

To run locally you can first start with

`
pip install -r requirements.txt
`

The first step will be to setup your database using

`
createdb Doricus
`

If you are not running a local postgres server or are renaming the database name to something else you will need the following environment variables to be set
`
export DB_NAME={your db name}
export DB_PATH={your postgres path}
`

Once that is setup you can proceed with creating your database by running
`
python manage.py db upgrade
`

Additionally we need to set the Authorization variables
`
export AUTH_DOMAIN={your auth0 domain}
export AUTH_AUDIENCE={your audience, default value is Doricus}
`

Now we are ready to run the backend locally
`
export FLASK_APP=app.py
flask run
`

## In Progress
More documentation will be added soon
You will be able to expect all API's to be documented