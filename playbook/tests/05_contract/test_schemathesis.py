import logging
from collections.abc import Iterator
from typing import Any

import pytest
import schemathesis as st
from django.urls import reverse
from schemathesis.specs.openapi.schemas import OpenApiSchema
from tracecov import CoverageMap
from tracecov.schemathesis import helpers

from server.wsgi import application


@pytest.fixture(autouse=True)
def _disable_logging() -> Iterator[None]:
    """Keep generated-case output focused on a failing interaction."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def api_schema(transactional_db: None) -> OpenApiSchema:
    """Load the live OpenAPI schema through Django's WSGI application."""
    return st.openapi.from_wsgi(reverse('openapi_json'), application)


schema = st.pytest.from_fixture('api_schema')


@pytest.mark.timeout(60)  # increase the default timeout for this test
@schema.parametrize()
def test_schemathesis(
    tracecov_map: CoverageMap,
    *,
    case: st.Case[Any],
) -> None:
    """Ensure that API implementation matches the OpenAPI schema."""
    response = case.call_and_validate()
    # Record interaction for `tracecov` report:
    tracecov_map.record_schemathesis_interactions(
        case.method,
        case.operation.full_path,
        [helpers.from_response(case.method, response)],
    )
