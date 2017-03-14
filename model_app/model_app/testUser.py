from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from model_app.models import Task, Review

import json

class TestUser(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        call_command("loaddata", "./model_app/db.json")
        pass #nothing to set up


    #----------------------Testing "user" ---------------------------
    def test_get_user_info(self):
        response = self.client.get(reverse('user_info', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_json['id'], 1)

    def test_get_user_info_incorrect_url(self):
        response = self.client.get('api/v1/user/info/')
        self.assertEquals(response.status_code, 404)

    def test_get_user_not_present(self):
        response = self.client.get(reverse('user_info', args=[68]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, 'ERROR: User with that id does not exist')

    def test_post_user_no_update(self):
        response = self.client.post(reverse('user_info', args=[1]), {})
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, {
                "id": 1,
                "fname": "TDawg",
                "lname": "Pinckney",
                "email": "fake@gmail.com",
                "bio": "I like to program",
                "pw": "password",
                "location": "Charlottesville"
            })

    def test_post_user_update_some_fields(self):
        response = self.client.post(reverse('user_info', args=[1]), {"fname": "New", "lname":"Name"})
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, {
                "id": 1,
                "fname": "New",
                "lname": "Name",
                "email": "fake@gmail.com",
                "bio": "I like to program",
                "pw": "password",
                "location": "Charlottesville"
            })
    def test_post_user_update_all_fields(self):
        response = self.client.post(reverse('user_info', args=[1]), {"fname": "New", "lname": "Name", "email": "new@gmail.com", "bio":"I make changes", "pw":"secret", "location":"Virginia"})
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, {
                "id": 1,
                "fname": "New",
                "lname": "Name",
                "email": "new@gmail.com",
                "bio": "I make changes",
                "pw": "secret",
                "location": "Virginia"
            })

    def test_delete_user(self):
        create_json = {
                "fname":'Dan',
                "lname":'Theman',
                "email":'xyz@example.com',
                "bio":"",
                "pw":'pas',
                "location":'behind you',
            }
        response = self.client.post(reverse('user_create'), create_json)
        resp_json = json.loads((response.content).decode("utf-8"))

        response2 = self.client.delete(reverse('user_info', args=[resp_json['id']]))
        resp2 = (response2.content).decode("utf-8")
        self.assertEquals(resp2, "Deleted User with ID: " + str(resp_json['id']))

        response3 = self.client.get(reverse('user_info', args=[resp_json['id']]))
        resp3 = (response3.content).decode("utf-8")
        self.assertEquals(resp3, "ERROR: User with that id does not exist")

    def test_delete_user_no_user(self):
        response = self.client.delete(reverse('user_info', args=[60]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: User with that id does not exist")

    # ------------------ Testing "user_create" --------------------------
    def test_post_create_user_no_fields(self):
        response = self.client.post(reverse('user_create'), {})
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertTrue(resp_json["ERROR"].startswith("Missing required fields:"))

    def test_post_create_user_some_fields(self):
        response = self.client.post(reverse('user_create'), {"fname": "1", "lname": "2"})
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertTrue(resp_json["ERROR"].startswith("Missing required fields:"))


    def test_post_create_user_all_fields(self):
        response = self.client.post(reverse('user_create'), {"fname": "1", "lname": "2", "email": "3", "bio": "4", "pw": "5", "location": "6" })
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json["fname"], "1")
        self.assertEquals(resp_json["lname"], "2")
        self.assertEquals(resp_json["email"], "3")
        self.assertEquals(resp_json["bio"], "4")
        self.assertEquals(resp_json["pw"], "5")
        self.assertEquals(resp_json["location"], "6")

    def test_get_create_user(self):
        response = self.client.get(reverse('user_create'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: User creation endpoint must be posted")

    # -----------------------Testing "user_languages"------------------------------
    def test_post_user_languages(self):
        response = self.client.post(reverse('user_languages', args=[1]), {})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_user_languages_no_user(self):
        response = self.client.get(reverse('user_languages', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_user_languages_correct(self):
        response = self.client.get(reverse('user_languages', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json[0]["spoken_language"], "English")
        self.assertEquals(resp_json[0]["id"], 1)
        self.assertEquals(resp_json[0]["user"], 1)

    # -----------------------Testing "user_skills" ------------------------------
    def test_post_user_skills(self):
        response = self.client.post(reverse('user_skills', args=[1]), {})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_user_skills_no_user(self):
        response = self.client.get(reverse('user_skills', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_user_skills_correct(self):
        response = self.client.get(reverse('user_skills', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json[0]["skill"], "Java")
        self.assertEquals(resp_json[0]["id"], 1)
        self.assertEquals(resp_json[0]["user"], 1)

    # -----------------------Testing "user_owner_tasks" ------------------------------
    def test_post_user_owners_task(self):
        response = self.client.post(reverse('user_owner_tasks', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_user_owners_task_no_user(self):
        response = self.client.get(reverse('user_owner_tasks', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_user_owners_task_correct(self):
        response = self.client.get(reverse('user_owner_tasks', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        taskFields = tuple(field.name for field in Task._meta.fields)
        for i in resp_json:
            for j in taskFields:
                self.assertEquals(j in i, True)

    # -----------------------Testing "user_worker_tasks" ------------------------------
    def test_post_user_workers_task(self):
        response = self.client.post(reverse('user_worker_tasks', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_user_workers_task_no_user(self):
        response = self.client.get(reverse('user_worker_tasks', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_user_workers_task_correct(self):
        response = self.client.get(reverse('user_worker_tasks', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        taskFields = tuple(field.name for field in Task._meta.fields)
        for i in resp_json:
            for j in taskFields:
                self.assertEquals(j in i, True)

    # -----------------------Testing "user_reviews" ------------------------------
    def test_post_user_reviews(self):
        response = self.client.post(reverse('user_reviews', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_user_reviews_no_user(self):
        response = self.client.get(reverse('user_reviews', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_user_reviews_correct(self):
        response = self.client.get(reverse('user_reviews', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        reviewFields = tuple(field.name for field in Review._meta.fields)
        for i in resp_json:
            for j in reviewFields:
                self.assertEquals(j in i, True)

    # -----------------------Testing "user_reviewed" ------------------------------
    def test_post_user_reviewed(self):
        response = self.client.post(reverse('user_reviewed', args=[1]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Can only accept GET requests")

    def test_get_user_reviewed_no_user(self):
        response = self.client.get(reverse('user_reviewed', args=[40])) 
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, [])

    def test_get_user_reviewed_correct(self):
        response = self.client.get(reverse('user_reviewed', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        reviewFields = tuple(field.name for field in Review._meta.fields)
        for i in resp_json:
            for j in reviewFields:
                self.assertEquals(j in i, True)


    

    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
