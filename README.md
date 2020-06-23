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
- Request authorization: get:account
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
- Request authorization: post:account
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
- Request authorization: update:account
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
- This operation returns all the projects to which a member is attached to
- The member is deduced from the Authorization token
- Validations: 
    - Check if member exists
- Request authorization: get:projects
- Request arguments: None
- Request headers: Authorization token
- Response data: the request returns an object in which 2 lists of projects are provided along with the counts for each list. Each list will contain objects of each project either still open or closed based on the end date of the project.
{
    'success':True,
    'openProjects': [],
    'closedProjects':[],
    'openProjectCount':0,
    'closedProjectCount':0
}
```

#### GET '/projects/<project_id>'
```
- This operation returns a single project if the member is attached to it
- The member is deduced from the Authorization token
- Validations:
    - Member is attached to project member list
- Request authorization: get:projects
- Request arguments: project id
- Request headers: Authorization token
- Response data: the request returns a full project object along with all the topics and comments of the project
{
    'success':True,
    'project':{}
}
```

#### POST '/projects'
```
- This operation 
- The member is deduced from the Authorization token
- Validations:
    - Member is existing
    - Project data is provided
- Request authorization: post:projects
- Request arguments: None
- Request headers: Authorization token
- Request data: The operation returns the newly created project
{
    'project':{}
}
- Response data: 
{
    'success':True,
    'project':{}
}
```

#### PATCH '/projects/<project_id>'
```
- This operation updates an existing project id with the data provided
- This operation can only be performed by the owner of the project
- The member is deduced from the Authorization token
- Validations:
    - Member exists
    - Project id exists
    - If the member is not the same as the project's owner
- Request authorization: patch:projects
- Request arguments: project id
- Request headers: Authorization token
- Request data:
{
    'project':{}
}
- Response data: The response will contain the updated project
{
    'success':True,
    'project':{}
}
```

#### DELETE '/projects/<project_id>'
```
- This operation deletes a given project
- This operation can only be performed by the owner of the project
- The member is deduced from the Authorization token
- Validations:
    - Member exists
    - Project exists
    - Member is project owner
- Request authorization: delete:projects
- Request arguments: project id
- Request headers: Authorization token
- Response data: 
{
    'success':True,
    'project_id':0
}
```

### Topics
#### GET '/projects/<project_id>/topics/<topic_id>'
```
- This operation returns all the information of a single topic, including the comments
- The member is deduced from the Authorization token
- Validations:
    - Member exists
    - Member is attached to the project
    - Project exists
- Request authorization: get:topics
- Request arguments: project id, topic id
- Request headers: Authorization token
- Response data: The request returns an object which includes the topic object along with a list of all the comments
{
    'success':True,
    'topic':{}
}
```

#### POST '/projects/<project_id>/topics'
```
- This operation creates a new topic for the given project id
- The member is deduced from the Authorization token
- Validations:
    - Member exists
    - Topic data is provided
    - Member is attached to project
    - Project exists
- Request authorization: post:topics
- Request arguments: project id
- Request headers: Authorization token
- Request data:
{
    'topic':{}
}
- Response data: The response contains the topic object that was just created
{
    'success':True,
    'topic':{}
}
```

#### PATCH '/topics/<topic_id>'
```
- This operation allows the topic owner to update the given topic's visibility
- The member is deduced from the Authorization token
- Validations:
    - Member is topic owner
    - Topic exists
- Request authorization: patch:topics
- Request arguments: topic id
- Request headers: Authorization token
- Request data:
{
    'topic':{
        'visibility':''
    }
}
- Response data: The request returns the updated topic
{
    'success':True,
    'topic':{ }
}
```

#### DELETE '/topics/<topic_id>'
```
- This operation allows the topic owner to delete the given topic
- The member is deduced from the Authorization token
- Validations:
    - Member is topic owner
    - Topic exists
- Request authorization: delete:topics
- Request arguments: topic id
- Request headers: Authorization token
- Response data: The request returns the updated topic
{
    'success':True,
    'topic_id':0
}
```

### Topic Comments
#### POST '/projects/<project_id>/topics/<topic_id>/comments'
```
- This operation posts a new comment to the provided project and topic.
- The member is deduced from the Authorization token
- Validations:
    - Comment data is provided
    - Topic exists
    - Member exists
    - Project exists
    - Member is attached to project
- Request authorization: post:comments
- Request arguments: project id, topic id
- Request headers: Authorization code
- Request data:
{
    'comment':{}
}
- Response data: The response returns the newly created comment 
{
    'success':True,
    'comment':{}
}
```

### Roles and Permissions
#### Architect
The architect role is the most complete role of all, it contains all of the actions to deal with the projects and topics
Permissions for the role:
- delete:projects	Remove projects	
- delete:topics	Remove topics	
- get:account	Get Account info	
- get:comments	Read comments on topic	
- get:projects	Read projects	
- get:topics	Read topics	
- patch:account	Update account info	
- patch:projects	Update projects	
- patch:topics	Update topics	
- post:account	Create account info
- post:comments	Create comments	
- post:projects	Create projects	
- post:topics	Create topics

#### Builder
The builder role is the second level in the applicaiton, it helps support the architect role so both can communicate
Permissions for the role:
- delete:topics	    Remove topics	
- get:account	    Get Account info	
- get:comments	    Read comments on topic	
- get:projects	    Read projects	
- get:topics	    Read topics	
- patch:account	    Update account info	
- patch:topics	    Update topics	
- post:account	    Create account info	
- post:comments	    Create comments	
- post:topics	    Create topics

#### Customer
The customer role is basicaly more like an observer role and gives the user the opportunity to view the assigned projects and open topics
Permissions for the role:
- get:account	    Get Account info
- patch:account	    Update account info
- post:account	    Create account info
- get:projects	    Read projects
- get:topics	    Read topics
- post:comments     Create comments
- get:comments	    Read comments on topic

### Error Codes

- 404: Resource not found
- 405: Method not allowed
- 422: Resource cannot be processed
- 400: Bad request
- 500: Request not allowed

## Testing
To run the tests, run
```
dropdb doricus_test
createdb doricus_test
psql doricus_test < doricus_test.psql
python test_app.py
```