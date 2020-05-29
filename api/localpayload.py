import os

app_env = os.environ.get('FLASK_ENV', 'production')

if app_env == 'development':
  #temporary while Authentication is not used
  payload = {
    'sub':'auth0|5ead88c11cc1ac0c147df5c8'
  }