from dmr.openapi import OpenAPIConfig, build_schema
from dmr.openapi.views import OpenAPIJsonView, SwaggerView
from dmr.routing import Router, path

router = Router(prefix='api/')

schema = build_schema(
    router,
    config=OpenAPIConfig(
        title='DMR testing playbook API',
        version='0.1.0',
        description=(
            'Real-world testing patterns, tools, and practices '
            'for django-modern-rest'
        )
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
