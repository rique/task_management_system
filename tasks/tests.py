import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tasks.models import Task
from rest_framework_simplejwt.tokens import RefreshToken

# Provides a pre-initialized APIClient instance
@pytest.fixture
def api_client():
    return APIClient()

# Creates a test user with a username and password
@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='testpassword')

# Creates an authenticated API client
@pytest.fixture
def authenticated_client(api_client, test_user):
    refresh = RefreshToken.for_user(test_user) # Creates a refresh and access token for the test user
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}') # Adds the credentials to the API client
    return api_client

# Test of new task creation via the POST endpoint
@pytest.mark.django_db
def test_create_task(authenticated_client):
    data = {'title': 'Test Task', 'description': 'Test Description'} # Data for an unasign task
    response = authenticated_client.post('/api/tasks/', data, format='json')
    # Asserting reeponse code is 201 
    # Number of tasks is 1
    # And the title is correct
    assert response.status_code == 201 # HTTP code 201 Created 
    assert Task.objects.count() == 1
    assert Task.objects.first().title == 'Test Task'

# Tests for listings all tasks
@pytest.mark.django_db
def test_get_tasks(authenticated_client):
    # Creating 2 task objects into the database
    Task.objects.create(title='Task 1', assigned_to=User.objects.first())
    Task.objects.create(title='Task 2', assigned_to=User.objects.first())
    response = authenticated_client.get('/api/tasks/') # Calling the API
    assert response.status_code == 200 # Asserting response status code is 200
    assert len(response.data['results']) == 2 # Asserting number of tasks is 2

# Testing for getting a single task by its id
@pytest.mark.django_db
def test_get_single_task(authenticated_client):
    task = Task.objects.create(title='Single Task', assigned_to=User.objects.first())
    response = authenticated_client.get(f'/api/tasks/{task.id}/')
    assert response.status_code == 200
    assert response.data['title'] == 'Single Task'

# Updateting a task with the PATCH method
@pytest.mark.django_db
def test_update_task(authenticated_client):
    task = Task.objects.create(title='Old Title', assigned_to=User.objects.first())
    data = {'title': 'New Title'}
    response = authenticated_client.patch(f'/api/tasks/{task.id}/', data, format='json')
    assert response.status_code == 200
    assert Task.objects.get(id=task.id).title == 'New Title'

# Testing deleting a task
@pytest.mark.django_db
def test_delete_task(authenticated_client):
    task = Task.objects.create(title='Task to Delete', assigned_to=User.objects.first())
    response = authenticated_client.delete(f'/api/tasks/{task.id}/')
    assert response.status_code == 204 # HTTP code 204 No Content 
    assert Task.objects.count() == 0


# Testing filtering task by completed status
@pytest.mark.django_db
def test_filter_tasks_by_completed(authenticated_client):
    Task.objects.create(title='Completed Task', completed=True, assigned_to=User.objects.first())
    Task.objects.create(title='Incomplete Task', completed=False, assigned_to=User.objects.first())
    response = authenticated_client.get('/api/tasks/?completed=true')
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'Completed Task'


# Testing filetring tasks by due date
@pytest.mark.django_db
def test_filter_tasks_by_due_date(authenticated_client):
    from datetime import date, timedelta
    today = date.today()
    tomorrow = today + timedelta(days=1)
    Task.objects.create(title='Today Task', due_date=today, assigned_to=User.objects.first())
    Task.objects.create(title='Tomorrow Task', due_date=tomorrow, assigned_to=User.objects.first())
    response = authenticated_client.get(f'/api/tasks/?due_date={today}')
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'Today Task'


# Test ordering tasks by due date
@pytest.mark.django_db
def test_order_tasks_by_due_date(authenticated_client):
    from datetime import date, timedelta
    today = date.today()
    tomorrow = today + timedelta(days=1)
    Task.objects.create(title='Tomorrow Task', due_date=tomorrow, assigned_to=User.objects.first())
    Task.objects.create(title='Today Task', due_date=today, assigned_to=User.objects.first())
    response = authenticated_client.get('/api/tasks/?ordering=due_date')
    assert response.status_code == 200
    assert response.data['results'][0]['title'] == 'Today Task'
