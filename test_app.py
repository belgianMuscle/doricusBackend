import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import app
from database.models import setup_db

JWT = os.environ.get('TEST_JWT',{'bearer':'test'})

class DoricusTestCases(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.app
        self.client = self.app.test_client
        #self.database_name = "Doricus_test"
        #self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'udacity','localhost:5432', self.database_name)
        #setup_db(self.app, self.database_path, True)

        # binds the app to the current context
        #with self.app.app_context():
            #self.db = SQLAlchemy()
            #self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_projects(self):
        res = self.client().get('/', headers={'Authorization':JWT})
        print(res)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()