from test_login import BaseTestCase
import datetime
from book.models import Question
import json


class QuestionTest(BaseTestCase):
    def test_question(self):
        self.url = '/book/question/'
        data = {
            "question": "hhh"
        }
        name_list = Question.objects.values_list('question_text')
        self.assertNotIn(data['question'], name_list)
        response = self.client.post(self.url, json.dumps(data))
        self.assertEqual(response.status_code, 200)
        new_names = Question.objects.values('question_text')
        name_lists = [name['question_text'] for name in new_names]
        self.assertIn(data['question'], name_lists)
