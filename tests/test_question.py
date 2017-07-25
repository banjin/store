from test_login import BaseTestCase
import datetime
from book.models import Question
import json


class QuestionTest(BaseTestCase):
    def test_question(self):
        self.url = '/book/question/'
        data = {
            "question_text": "hhh",
            "pub_date":datetime.datetime.now()
        }
        name_list = Question.objects.values_list('question_text')
        self.assertNotIn(data['question_text'], name_list)
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        new_names = Question.objects.values('question_text')
        name_lists = [name['question_text'] for name in new_names]
        self.assertNotIn(data['question_text'], name_lists)
