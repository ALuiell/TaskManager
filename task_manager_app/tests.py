from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager_app.models import Project, Task


# Create your tests here.
class ProjectCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.url = reverse("add_project")

    def test_create_project_success(self):
        response = self.client.post(self.url, {"name": "New Project"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, "New Project")
        self.assertEqual(project.user, self.user)

    def test_create_project_missing_name(self):
        response = self.client.post(self.url, {"name": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.count(), 0)

    def test_update_project_success(self):
        response = self.client.post(self.url, {"name": "New Project"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        update_url = reverse("update_project", kwargs={"project_id": project.id})
        response = self.client.post(update_url, {"name": "Updated Project Name"})
        self.assertEqual(response.status_code, 200)
        project.refresh_from_db()
        self.assertEqual(project.name, "Updated Project Name")

    def test_update_project_missing_name(self):
        response = self.client.post(self.url, {"name": "New Project"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        update_url = reverse("update_project", kwargs={"project_id": project.id})
        response = self.client.post(update_url, {"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_delete_project_success(self):
        response = self.client.post(self.url, {"name": "New Project"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        delete_url = reverse("delete_project", kwargs={"project_id": project.id})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 0)


class TaskCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.project = Project.objects.create(name="Test Project", user=self.user)
        self.url = reverse('add_task', kwargs={"project_id": self.project.id})

    def test_create_task_success(self):
        response = self.client.post(self.url, {
            "name": "New Task",
            "status": "New",
            "priority": "1",
            "deadline": ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.filter(project=self.project).first()
        self.assertEqual(task.name, "New Task")
        self.assertEqual(task.project.user, self.user)
        self.assertEqual(task.status, Task.NEW)
        self.assertEqual(task.priority, 1)
        self.assertIsNone(task.deadline)

    def test_create_task_missing_name(self):
        response = self.client.post(self.url, {"name": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_defaults(self):
        response = self.client.post(self.url, {
            "name": "Default Task",
            'priority': '',
            'deadline': '',
            'status': ''})
        self.assertEqual(response.status_code, 302)
        task = Task.objects.first()
        self.assertNotEqual(Task.objects.count(), 0)
        self.assertEqual(task.priority, 2)
        self.assertEqual(task.status, Task.NEW)

    def test_update_task_success(self):
        response = self.client.post(self.url, {
            "name": "New Task",
            "status": "New",
            "priority": "1",
            "deadline": ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.filter(project=self.project).first()
        self.assertIsNotNone(task)
        self.assertEqual(task.name, "New Task")
        self.assertEqual(task.status, Task.NEW)
        self.assertEqual(task.priority, 1)
        self.assertIsNone(task.deadline)

        update_url = reverse("update_task", kwargs={"task_id": task.id})

        response = self.client.post(update_url, {
            "name": "Updated Task",
            "status": "in_progress",
            "priority": "2",
            "deadline": "2025-12-31T12:00"
        })
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Task")
        self.assertEqual(task.status, Task.IN_PROGRESS)
        self.assertEqual(task.priority, 2)
        self.assertEqual(task.deadline.strftime("%Y-%m-%dT%H:%M"), "2025-12-31T12:00")

    def test_delete_task_success(self):
        response = self.client.post(self.url, {
            "name": "New Task",
            "status": "New",
            "priority": "1",
            "deadline": ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.filter(project=self.project).first()
        response = self.client.post(reverse("delete_task", kwargs={"task_id": task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)