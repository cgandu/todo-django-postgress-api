from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task

class TaskModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_task_creation(self):
        task = Task.objects.create(user=self.user, content="Test task")
        self.assertEqual(str(task), "Test task")
        self.assertFalse(task.completed)
