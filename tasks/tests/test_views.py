from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from tasks.models import Task

class TaskViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        response = self.client.post('/api/tasks/', {'content': 'Test task'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().content, 'Test task')

    def test_get_tasks(self):
        Task.objects.create(user=self.user, content='Test task 1')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test task 1')
