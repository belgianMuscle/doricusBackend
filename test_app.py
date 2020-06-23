import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy

import app
from database.models import setup_db, getCurrentTime

JWT = os.environ.get('TEST_JWT', {'bearer': 'test'})


class DoricusTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.remove('database.db')
        except:
            print('no database file exists yet')

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.app
        self.client = self.app.test_client
        self.database_path = 'sqlite:///database.db'
        setup_db(self.app, self.database_path, True)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_account(self):
        idata = {
            'member': {
                'full_name': 'Test',
                'email': 'test@test.com',
                'type': 'ARCHITECT'
            }
        }

        res = self.client().post('/members',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])
    
    def test_create_account_wo_data(self):
        res = self.client().post('/members', headers={'Authorization': JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"No account data provided")
    
    def test_create_account_wo_auth(self):
        res = self.client().post('/members', headers={'Authorization': ''})

        self.assertEqual(res.status_code, 401)

    def test_create_project(self):
        idata = {
            'project': {
                'title': 'Test 1',
                'description': 'Test Project number 1',
                'image_url': 'http://test_url.com',
                'start_date': '2020-01-01 10:00:00',
                'proj_end_date': '2020-10-01 10:00:00',
                'act_end_date': '2020-12-01 10:00:00',
                'address': 'Test Address'
            }
        }

        res = self.client().post('/projects',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])
    
    def test_create_project_wo_data(self):
        idata = {
            'project': { }
        }

        res = self.client().post('/projects',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
    
    def test_update_project(self):
        idata = {
            'project': {
                'title': 'Test Update 1',
                'description': 'Test Project update number 1',
                'image_url': 'http://test_url.com',
                'start_date': '2020-01-01 10:00:00',
                'proj_end_date': '2020-10-01 10:00:00',
                'act_end_date': '2020-12-01 10:00:00',
                'address': 'Test Address'
            }
        }

        res = self.client().patch('/projects/1',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])
    
    def test_update_wrong_project(self):
        idata = {
            'project': {
                'title': 'Test Update 1',
                'description': 'Test Project update number 1',
                'image_url': 'http://test_url.com',
                'start_date': '2020-01-01 10:00:00',
                'proj_end_date': '2020-10-01 10:00:00',
                'act_end_date': '2020-12-01 10:00:00',
                'address': 'Test Address'
            }
        }

        res = self.client().patch('/projects/99',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_projects(self):
        res = self.client().get('/projects', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['openProjects'])
        self.assertEqual(len(data['closedProjects']),0)
        self.assertEqual(data['openProjectCount'], 1)
        self.assertEqual(data['closedProjectCount'], 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
