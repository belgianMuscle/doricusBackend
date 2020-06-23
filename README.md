# Doricus - Backend

## Introduction
Welcome to the Doricus Backend. Doricus is a Construction Management Platform which is meant to help Architects, Builders and Customers communicate and track progress. More information about Doricus can be found at: URL to come. 

This backend has been developed with Python using the Flask framework. We are currently using a Postgres database to host all the data necessary for the app to work. 
Additionally we are using Auth0 for authentication and role based permissions.

This backend is meant to be accessible as an API for the frontend. CORS will only be available to the appropriate resources.

### Motivation
The motivation of this project is to help my partner who is an Architect to communicate with her contractors and customers. While there are many options out for communication of random topics, this project was intended to provide a more specialized platform to facilitate this communication.

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

## Deployment
This project has been built to be deployed on Heroku as a Python app. The project needs the postgresql add-on to be installed on the instance as well.
Along with the regular instance configuration, the following environment variables need to be configured:
- AUTH_AUDIENCE
- AUTH_DOMAIN
- DATABASE_URL (automatically set by Heroku postgresql add-on package)

## Current Deployment
The current version of the project is hosted through Heroku on url:
```
https://doricus-backend.herokuapp.com/
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
    'member':{
        'id':0,
        'auth0_id':'',
        'full_name':'',
        'email':'',
        'type':''
    }
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
    'member':{
        'full_name':'',
        'email':'',
        'type':''
    }
}
- Returns the created member object
{ 
    'success':True,
    'member':{
        'id':0,
        'auth0_id':'',
        'full_name':'',
        'email':'',
        'type':''
    }
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
    'member':{
        'full_name':'',
        'email':'',
        'type':''
    }
}
- Returns the created member object
{ 
    'success':True,
    'member':{
        'id':0,
        'auth0_id':'',
        'full_name':'',
        'email':'',
        'type':''
    }
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
    'openProjects': [{
        'id': '',
        'member_id': '',
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
    }],
    'closedProjects':[{
        'id': '',
        'member_id': '',
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
    }],
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
    'project':{
        'id': '',
        'member_id': '',
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
        'topics':[]
    }
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
    'project':{
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
    }
}
- Response data: 
{
    'success':True,
    'project':{
        'id': '',
        'member_id': '',
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
    }
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
    'project':{
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
    }
}
- Response data: The response will contain the updated project
{
    'success':True,
    'project':{
        'id': '',
        'member_id': '',
        'title': '',
        'description': '',
        'image_url': '',
        'start_date': '',
        'proj_end_date': '',
        'act_end_date': '',
        'address': ''
    }
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
    'success': True,
    'project_id': 0
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
    'topic':{
        'id': '',
        'project_id': '',
        'member_id': '',
        'timestamp': '',
        'title': '',
        'type': '',
        'event_date': '',
        'content': '',
        'visibility': '',
        'comments': []
    }
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
    'topic':{
        'timestamp': '',
        'title': '',
        'type': '',
        'event_date': '',
        'content': '',
        'visibility': ''
    }
}
- Response data: The response contains the topic object that was just created
{
    'success':True,
    'topic':{
        'id': '',
        'project_id': '',
        'member_id': '',
        'timestamp': '',
        'title': '',
        'type': '',
        'event_date': '',
        'content': '',
        'visibility': '',
        'comments': []
    }
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
    'topic':{
        'id': '',
        'project_id': '',
        'member_id': '',
        'timestamp': '',
        'title': '',
        'type': '',
        'event_date': '',
        'content': '',
        'visibility': '',
        'comments': []
    }
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
    'comment':{
        'timestamp':'',
        'content':''
    }
}
- Response data: The response returns the newly created comment 
{
    'success':True,
    'comment':{
        'id': '',
        'topic_id': '',
        'member_id': '',
        'timestamp': '',
        'content': ''
    }
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
To run the tests, first generate an Authorization token. 
The Authorization token needs to be saved as an environment variable like follows:
```
export TEST_JWT="bearer {token}"
```
With this token, you can now run the tests.
```
python test_app.py
```