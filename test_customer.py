import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy

import app
from database.models import setup_db, getCurrentTime

JWT = os.environ.get('TEST_CUST_JWT', "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFac3d4NG0zZEtReUtRNTR6QllNMiJ9.eyJpc3MiOiJodHRwczovL2JlbGdpYW5tdXNjbGUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTYxY2VkNzFhZjBiMGM2ZTQ2YzllNyIsImF1ZCI6WyJodHRwczovL2RvcmljdXMuaGVyb2t1LmNvbS8iLCJodHRwczovL2JlbGdpYW5tdXNjbGUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MzAxMzkwNSwiZXhwIjoxNTkzMDIxMTA1LCJhenAiOiJ3REx1d0ZFNXhrd01zWjZibFpieHJCTUdxdXYxRTl0SyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dG9waWNzIiwiZ2V0OmFjY291bnQiLCJnZXQ6Y29tbWVudHMiLCJnZXQ6cHJvamVjdHMiLCJnZXQ6dG9waWNzIiwicGF0Y2g6YWNjb3VudCIsInBhdGNoOnRvcGljcyIsInBvc3Q6YWNjb3VudCIsInBvc3Q6Y29tbWVudHMiLCJwb3N0OnRvcGljcyJdfQ.Erz7VZ9wxiLTEIXHdJQP5grGUj_k4llUIQZVQvuLWaNxslGjZTDF7zGuCx-tU-KaFqczZpF-uZQoCsz6IPJ79nWLEKMqQIdtKKbOw6UC87XiiAEd-IIbEJVa179HQly-8IkddkxDzryZD1Vfn6_3oQug0GM4y80RtWo815h6YVOzL2NY_JS_sg2hg5j7S4NvCdJOOuG92HOH6zR9EYtoit7k6hJ-qyLIa4tQFJxlhQLotMCNvJTTRun6vOVIxZd70BOUXH9a4Himyb90ePuFPyScyLgRaiYo2Fz1HNsDDkW77bqepAhxT23ikgU2D0e5j8-sr1ZcvSmj7F63c3K0dg")

class DoricusCustomerTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            copyfile('test_db_customer_original.db', 'test_db_customer.db')
        except:
            print('no database file exists yet')

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.app
        self.client = self.app.test_client
        self.database_path = 'sqlite:///test_db_customer.db'
        setup_db(self.app, self.database_path, True)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    #
    # Create Account
    #
    def test_1_create_account(self):
        print('Running test 1')
        idata = {
            'member': {
                'full_name': 'Test',
                'email': 'test@test.com',
                'type': 'CUSTOMER'
            }
        }

        res = self.client().post('/members',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])
    
        #
    # Create a new project  -> Builder is not allowed to create projects
    #
    def test_2_create_project(self):
        print('Running test 2')
        idata = {
            'project': {
                'title': 'Test 1',
                'description': 'Test Project number 1',
                'image_url': 'http://test_url.com',
                'start_date': '2020-01-01',
                'proj_end_date': '2020-10-01',
                'act_end_date': '2020-12-01',
                'address': 'Test Address'
            }
        }

        res = self.client().post('/projects',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 403)
    

    #
    # Update an existing project -> Builder is not allowed to update project
    #
    def test_3_update_project(self):
        print('Running test 3')
        idata = {
            'project': {
                'title': 'Test Update 1',
                'description': 'Test Project update number 1',
                'image_url': 'http://test_url.com',
                'start_date': '2020-01-01',
                'proj_end_date': '2020-10-01',
                'act_end_date': '2020-12-01',
                'address': 'Test Address'
            }
        }

        res = self.client().patch('/projects/1',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 403)

    #
    #  Create a new topic -> Customer is not allowed to create topics
    #
    def test_4_create_topic(self):
        print('Running test 4')
        idata = {
            'topic':{
                'timestamp': '2020-06-22 10:00:00',
                'title': 'First post',
                'type': 'TEXT',
                'event_date': '2020-01-01',
                'content': 'This is the content of the topic',
                'visibility': 'CLOSED'
            }
        }

        res = self.client().post('/projects/1/topics',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 403)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DoricusCustomerTestCases('test_1_create_account'))
    suite.addTest(DoricusCustomerTestCases('test_2_create_project'))
    suite.addTest(DoricusCustomerTestCases('test_3_update_project'))
    suite.addTest(DoricusCustomerTestCases('test_4_create_topic'))

    return suite


# Make the tests conveniently executable
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())