from django.test import TestCase
from tasks.serializers import TaskSerializer
from tasks.models import Task
from django.contrib.auth.models import User

class TaskSerializerTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.task = Task.objects.create(user=cls.user, content="Test task")

    def test_task_serialization(self):
        serializer = TaskSerializer(self.task)
        data = serializer.data
        self.assertEqual(data['content'], 'Test task')
        self.assertEqual(data['completed'], False)

    def test_task_deserialization(self):
        data = {'content': 'New task'}
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['content'], 'New task')
