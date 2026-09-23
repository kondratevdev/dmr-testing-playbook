from dmr.openapi import OpenAPIConfig, build_schema
from dmr.openapi.views import OpenAPIJsonView, SwaggerView
from dmr.plugins.msgspec import MsgspecSerializer
from dmr.routing import Router, build_404_handler, path

from server.apps.tasks.api import urls as task_urls

router = Router(prefix='api/')
router.include(task_urls.router, namespace='tasks')

schema = build_schema(
    router,
    config=OpenAPIConfig(
        title='DMR testing playbook API',
        version='0.1.0',
        description=(
            'Real-world testing patterns, tools, and practices '
            'for django-modern-rest'
        ),
    ),
)

urlpatterns = [
    router.to_urlpatterns(namespace='api'),
    path(
        'docs/openapi.json/',
        OpenAPIJsonView.as_view(schema),
        name='openapi_json',
    ),
    path('docs/swagger/', SwaggerView.as_view(schema), name='swagger'),
]

handler404 = build_404_handler(
    router.prefix,
    serializer=MsgspecSerializer,
)
