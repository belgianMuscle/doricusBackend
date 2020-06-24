import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy

import app
from database.models import setup_db, getCurrentTime

JWT = os.environ.get('TEST_ARCH_JWT', {'bearer': 'test'})


class DoricusArchitectTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.remove('test_db_architect.db')
        except:
            print('no database file exists yet')

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.app
        self.client = self.app.test_client
        self.database_path = 'sqlite:///test_db_architect.db'
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
                'type': 'ARCHITECT'
            }
        }

        res = self.client().post('/members',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])
        
    #
    # Create Account - without data -> expects a failure
    #
    def test_2_create_account_wo_data(self):
        print('Running test 2')
        res = self.client().post('/members', headers={'Authorization': JWT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],"No account data provided")
            
    #
    # Create Account - without authorization -> expects a failure 
    #
    def test_3_create_account_wo_auth(self):
        print('Running test 3')
        res = self.client().post('/members', headers={'Authorization': ''})

        self.assertEqual(res.status_code, 401)
    
    #
    # Get account 
    #
    def test_4_get_account(self):
        print('Running test 4')
        res = self.client().get('/members', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

    #
    # Get account without authorization 
    #
    def test_5_get_account_wo_auth(self):
        print('Running test 5')
        res = self.client().get('/members', headers={'Authorization': ''})
        
        self.assertEqual(res.status_code, 401)

    #
    # Update Account
    #
    def test_5_2_update_account(self):
        print('Running test 1')
        idata = {
            'member': {
                'full_name': 'Test Updated',
                'email': 'test@test.com',
                'type': 'BUILDER'
            }
        }

        res = self.client().patch('/members/1',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

    #
    # Update Wrong Account
    #
    def test_5_3_update_wrong_account(self):
        print('Running test 1')
        idata = {
            'member': {
                'full_name': 'Test Updated',
                'email': 'test@test.com',
                'type': 'ARCHITECT'
            }
        }

        res = self.client().patch('/members/99',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 404)

    #
    # Update Account
    #
    def test_5_4_update_account_back_to_arch(self):
        print('Running test 1')
        idata = {
            'member': {
                'full_name': 'Test Updated',
                'email': 'test@test.com',
                'type': 'ARCHITECT'
            }
        }

        res = self.client().patch('/members/1',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['member'])

    #
    # Create a new project 
    #
    def test_6_create_project(self):
        print('Running test 6')
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
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])
            
    #
    # Create a new project - without data -> expects a failure 
    #
    def test_7_create_project_wo_data(self):
        print('Running test 7')
        idata = {
            'project': { }
        }

        res = self.client().post('/projects',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 400)
            
    #
    # Update an existing project 
    #
    def test_8_update_project(self):
        print('Running test 8')
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
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])
            
    #
    # Update a non-existing project -> expects a failure 
    #
    def test_9_update_wrong_project(self):
        print('Running test 9')
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

        res = self.client().patch('/projects/99',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 404)
        
    #
    # Get projects for current user
    #
    def test_10_get_projects(self):
        print('Running test 10')
        res = self.client().get('/projects', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['openProjects'])
        self.assertEqual(len(data['closedProjects']),0)
        self.assertEqual(data['openProjectCount'], 1)
        self.assertEqual(data['closedProjectCount'], 0)

    #
    # Get a specific project
    #
    def test_11_get_specific_project(self):
        print('Running test 11')
        res = self.client().get('/projects/1', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['project'])

    #
    # Get a non-existing project -> expects a failure 
    #
    def test_12_get_non_existing_project(self):
        print('Running test 12')
        res = self.client().get('/projects/99', headers={'Authorization': JWT})
        
        self.assertEqual(res.status_code, 404)

    #
    #  Create a new topic
    #
    def test_13_create_topic(self):
        print('Running test 13')
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
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['topic'])
    #
    # Create a new topic on a non-existing project -> expects a failure
    #
    def test_14_create_topic_wrong_project(self):
        print('Running test 14')
        idata = {
            'topic':{
                'timestamp': '2020-06-22 10:00:00',
                'title': 'Wrong post',
                'type': 'TEXT',
                'event_date': '2020-01-01',
                'content': 'This is the content of the topic',
                'visibility': 'CLOSED'
            }
        }

        res = self.client().post('/projects/99/topics',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 404)

    #
    # Create a new comment  
    #
    def test_15_create_comment(self):
        print('Running test 15')
        idata = {
            'comment':{
                'timestamp': '2020-06-22 10:00:00',
                'content': 'This is the first comment'
            }
        }

        res = self.client().post('/projects/1/topics/1/comments',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['comment'])

    #
    # Create a comment on a non-existing topic -> expects a failure  
    #
    def test_16_create_comment_wrong_topic(self):
        print('Running test 16')
        idata = {
            'comment':{
                'timestamp': '2020-06-22 10:00:00',
                'content': 'This is a wrong comment'
            }
        }

        res = self.client().post('/projects/1/topics/99/comments',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 404)

    #
    # Get project with topics and comments  
    #
    def test_17_get_project_with_topics_comments(self):
        print('Running test 17')
        res = self.client().get('/projects/1', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #
    #  Update an existing topic
    #
    def test_18_update_topic(self):
        print('Running test 18')
        idata = {
            'topic':{
                'visibility': 'OPEN'
            }
        }

        res = self.client().patch('topics/1',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['topic'])

    #
    #  Update an non-existing topic
    #
    def test_19_update_non_existing_topic(self):
        print('Running test 19')
        idata = {
            'topic':{
                'visibility': 'OPEN'
            }
        }

        res = self.client().patch('topics/99',data=json.dumps(idata), headers={'Authorization': JWT,'Content-Type': 'application/json'})

        self.assertEqual(res.status_code, 404)

    #
    #  Delete an existing topic
    #
    def test_20_delete_topic(self):
        print('Running test 20')
        res = self.client().delete('/topics/1', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['topic_id'],'1')

    #
    #  Delete a non-existing topic -> expects a failure
    #
    def test_21_delete_wrong_topic(self):
        print('Running test 21')
        res = self.client().delete('/topics/99', headers={'Authorization': JWT})
        
        self.assertEqual(res.status_code, 404)

    #
    #  Delete an existing project
    #
    def test_22_delete_project(self):
        print('Running test 22')
        res = self.client().delete('/projects/1', headers={'Authorization': JWT})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['project_id'],'1')

    #
    # Delete a non-existing project -> expects a failure 
    #
    def test_23_delete_wrong_project(self):
        print('Running test 23')
        res = self.client().delete('/projects/99', headers={'Authorization': JWT})
        
        self.assertEqual(res.status_code, 404)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DoricusTestCases('test_1_create_account'))
    suite.addTest(DoricusTestCases('test_2_create_account_wo_data'))
    suite.addTest(DoricusTestCases('test_3_create_account_wo_auth'))
    suite.addTest(DoricusTestCases('test_4_get_account'))
    suite.addTest(DoricusTestCases('test_5_get_account_wo_auth'))
    suite.addTest(DoricusTestCases('test_5_2_update_account'))
    suite.addTest(DoricusTestCases('test_5_3_update_wrong_account'))
    suite.addTest(DoricusTestCases('test_5_4_update_account_back_to_arch'))
    suite.addTest(DoricusTestCases('test_6_create_project'))
    suite.addTest(DoricusTestCases('test_7_create_project_wo_data'))
    suite.addTest(DoricusTestCases('test_8_update_project'))
    suite.addTest(DoricusTestCases('test_9_update_wrong_project'))
    suite.addTest(DoricusTestCases('test_10_get_projects'))
    suite.addTest(DoricusTestCases('test_11_get_specific_project'))
    suite.addTest(DoricusTestCases('test_12_get_non_existing_project'))
    suite.addTest(DoricusTestCases('test_13_create_topic'))
    suite.addTest(DoricusTestCases('test_14_create_topic_wrong_project'))
    suite.addTest(DoricusTestCases('test_15_create_comment'))
    suite.addTest(DoricusTestCases('test_16_create_comment_wrong_topic'))
    suite.addTest(DoricusTestCases('test_17_get_project_with_topics_comments'))
    suite.addTest(DoricusTestCases('test_18_update_topic'))
    suite.addTest(DoricusTestCases('test_19_update_non_existing_topic'))
    suite.addTest(DoricusTestCases('test_20_delete_topic'))
    suite.addTest(DoricusTestCases('test_21_delete_wrong_topic'))
    suite.addTest(DoricusTestCases('test_22_delete_project'))
    suite.addTest(DoricusTestCases('test_23_delete_wrong_project'))

    return suite


# Make the tests conveniently executable
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
