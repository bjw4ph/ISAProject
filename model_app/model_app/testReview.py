from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from model_app.models import Task, Review, Users

import json

class TestReview(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        call_command("loaddata", "./model_app/db.json")
        pass #nothing to set up


    #----------------------Testing "review_info" ---------------------------
    def test_get_review(self):
        response = self.client.get(reverse('review_info', args=[1]))
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_json, {
            "id": 1,
            "title": "What a terrible programmer",
            "body": "He couldn't spell his own name",
            "score": 0.42,
            "task": 1,
            "poster_user": 1,
            "postee_user": 2
        })

    def test_get_review_not_present(self):
        response = self.client.get(reverse('review_info', args=[68]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Review with that id does not exist")

    def test_post_review_no_update(self):
        response = self.client.post(reverse('review_info', args=[1]), {})
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, {
                "id": 1,
                "title": "What a terrible programmer",
                "body": "He couldn't spell his own name",
                "score": 0.42,
                "task": 1,
                "poster_user": 1,
                "postee_user": 2
            })

    def test_post_review_update_some_fields(self):
        response = self.client.post(reverse('review_info', args=[1]), 
                {
                    "title": "New", 
                    "body":"Body"
                })
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, {
                "id": 1,
                "title": "New",
                "body": "Body",
                "score": 0.42,
                "task": 1,
                "poster_user": 1,
                "postee_user": 2
            })
    def test_post_review_update_all_fields(self):
        response = self.client.post(reverse('review_info', args=[1]), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 4,
                "poster_user": 2,
                "postee_user": 3
            })
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json, {
                "id": 1,
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 4,
                "poster_user": 2,
                "postee_user": 3
            })
    def test_post_review_update_wrong_task_id(self):
        response = self.client.post(reverse('review_info', args=[1]), {"task": 50})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Task object does not exist")

    def test_post_review_update_wrong_postee_user_id(self):
        response = self.client.post(reverse('review_info', args=[1]), {"postee_user": 50})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Postee User does not exist")

    def test_post_review_update_wrong_poster_user_id(self):
        response = self.client.post(reverse('review_info', args=[1]), {"poster_user": 50})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Poster User does not exist")

    def test_delete_review(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 2,
                "poster_user": 3,
                "postee_user": 4
            })
        resp_json = json.loads((response.content).decode("utf-8"))

        response2 = self.client.delete(reverse('review_info', args=[resp_json['id']]))
        resp2 = (response2.content).decode("utf-8")
        self.assertEquals(resp2, "Deleted Review with ID: " + str(resp_json['id']))

        response3 = self.client.get(reverse('review_info', args=[resp_json['id']]))
        resp3 = (response3.content).decode("utf-8")
        self.assertEquals(resp3, "ERROR: Review with that id does not exist")

    def test_delete_review_no_review(self):
        response = self.client.delete(reverse('review_info', args=[60]))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Review with that id does not exist")

    # ------------------ Testing "review_create" --------------------------
    def test_post_review_create_correct(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 4,
                "poster_user": 2,
                "postee_user": 3
            })
        resp_json = json.loads((response.content).decode("utf-8"))
        self.assertEquals(resp_json["title"], '1')
        self.assertEquals(resp_json["body"], '2')
        self.assertEquals(resp_json["score"], '3')
        self.assertEquals(resp_json["task"], 4)
        self.assertEquals(resp_json["poster_user"], 2)
        self.assertEquals(resp_json["postee_user"], 3)

    def test_post_create_review_no_task(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "poster_user": 2,
                "postee_user": 3
            })
        resp_json = (response.content).decode("utf-8")
        self.assertTrue(resp_json.startswith("Missing required fields:"))

    def test_post_create_review_no_poster_user(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 2,
                "postee_user": 3
            })
        resp_json = (response.content).decode("utf-8")
        self.assertTrue(resp_json.startswith("Missing required fields:"))

    def test_post_create_review_no_postee_user(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 2,
                "poster_user": 3
            })
        resp_json = (response.content).decode("utf-8")
        self.assertTrue(resp_json.startswith("Missing required fields:"))

    def test_post_review_create_task_id_doesnt_exist(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 100,
                "poster_user": 2,
                "postee_user": 3
            })
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Task object does not exist")

    def test_post_review_create_poster_user_id_doesnt_exist(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 2,
                "poster_user": 100,
                "postee_user": 3
            })
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Poster User does not exist")

    def test_post_review_create_postee_user_id_doesnt_exist(self):
        response = self.client.post(reverse('review_create'), {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 2,
                "poster_user": 2,
                "postee_user": 100
            })
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Postee User does not exist")

    def test_get_review_create(self):
        response = self.client.get(reverse('review_create'))
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Review Creation endpoint must be POSTed")

    # -----------------------Testing "review_all"------------------------------------
    def test_post_review_all(self):
        response = self.client.post(reverse('review_all'), {})
        resp_json = (response.content).decode("utf-8")
        self.assertEquals(resp_json, "ERROR: Endpoint only accepts GET requests")

    def test_get_review_all(self):
        response = self.client.get(reverse('review_all'))
        resp_json = json.loads((response.content).decode("utf-8"))
        reviewFields = tuple(field.name for field in Review._meta.fields)
        for i in resp_json:
            for j in reviewFields:
                self.assertEquals(j in i, True)
    #tearDown method is called after each test
    def tearDown(self):
        pass #nothing to tear down
