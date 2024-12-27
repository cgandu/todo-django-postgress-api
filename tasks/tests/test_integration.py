from datetime import timedelta
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Task
from rest_framework_simplejwt.tokens import AccessToken

class TaskIntegrationTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.task = Task.objects.create(user=self.user, content='Integration task')


    def test_create_task(self):
        response = self.client.post('/api/tasks/', {'content': 'New integration task'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)

    def test_retrieve_task(self):
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], 'Integration task')
    
    def test_list_tasks(self):
        Task.objects.create(user=self.user, content='Second task')
        not_user_task = Task.objects.create(content='Not user task')
    
        response = self.client.get(f'/api/tasks/')
        response_data = response.json()

        self.assertTrue(all(task['user'] == self.user.id for task in response_data))
        self.assertFalse(any(task['id'] == not_user_task.id for task in response_data))
        self.assertEqual(response.status_code, 200)
        

    def test_patch_task(self):
        response = self.client.patch(f'/api/tasks/{self.task.id}/', {'completed': True}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.get(id=self.task.id).completed)

    def test_delete_task(self):
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)

    def test_list_tasks_unauthenticated(self):
        self.client.credentials()

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_list_tasks_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['code'], 'token_not_valid')
    

    def test_list_tasks_expired_token(self):
        token = AccessToken.for_user(self.user)
        token.set_exp(lifetime=timedelta(seconds=-1))

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['code'], 'token_not_valid')


