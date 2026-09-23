from dmr.routing import Router, path

from server.apps.tasks.api import views

router = Router(
    'tasks/',
    [
        path('', views.TaskCreate.as_view(), name='task_create'),
        path('<int:id>/', views.TaskDetail.as_view(), name='task_detail'),
    ],
    tags=['tasks'],
)
