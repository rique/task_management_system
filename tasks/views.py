from rest_framework import (
    permissions, 
    filters
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend

# The TaskListCreateView handles both listing and creating tasks
# When sending a POST request to /api/tasks/ with JSON data (title, description, due_date, assigned_to_id), the TaskSerializer validates the data 
# Whereas GET requests list all the tasks 
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    # for data validation: If the data is valid the serializer creates a new Task object in the database when using a POST request
    # When using a GET request it creates a JSON representation of each task
    serializer_class = TaskSerializer 
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access the endpoint
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter] 
    filterset_fields = ['completed', 'due_date'] # filetring tasks by complete (/api/tasks/?completed=true) or due_date (/api/tasks/?due_date=2024-12-31)
    ordering_fields = ['due_date'] # Ordering tasks by due_date (ASC /api/tasks/?ordering=due_date; DESC /api/tasks/?ordering=-due_date)

# For reading (GET request), updating (PUT/PATCH request) and deleting tasks (DELETE request)
class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
