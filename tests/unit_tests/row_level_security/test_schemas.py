# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest
from marshmallow import ValidationError

from superset.row_level_security.schemas import (
    get_delete_ids_schema,
    openapi_spec_methods_override,
    RLSPostSchema,
    RLSPutSchema,
)


def test_get_delete_ids_schema_structure() -> None:
    assert get_delete_ids_schema == {"type": "array", "items": {"type": "integer"}}


def test_openapi_spec_methods_override_keys() -> None:
    expected = {"get", "get_list", "delete", "info"}
    assert set(openapi_spec_methods_override.keys()) == expected


def test_rls_post_schema_valid_regular(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "Test Rule",
        "filter_type": "Regular",
        "tables": [1],
        "roles": [1],
        "clause": "id = 1",
    }
    result = schema.load(data)
    assert result["name"] == "Test Rule"
    assert result["filter_type"] == "Regular"
    assert result["clause"] == "id = 1"


def test_rls_post_schema_valid_base(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "Base Rule",
        "filter_type": "Base",
        "tables": [1, 2],
        "roles": [1],
        "clause": "1 = 0",
    }
    result = schema.load(data)
    assert result["filter_type"] == "Base"


def test_rls_post_schema_rejects_invalid_filter_type(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "Test",
        "filter_type": "InvalidType",
        "tables": [1],
        "roles": [1],
        "clause": "id = 1",
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "filter_type" in exc_info.value.messages


def test_rls_post_schema_rejects_missing_name(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "filter_type": "Regular",
        "tables": [1],
        "roles": [1],
        "clause": "id = 1",
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "name" in exc_info.value.messages


def test_rls_post_schema_rejects_empty_tables(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "Test",
        "filter_type": "Regular",
        "tables": [],
        "roles": [1],
        "clause": "id = 1",
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "tables" in exc_info.value.messages


def test_rls_post_schema_rejects_missing_clause(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "Test",
        "filter_type": "Regular",
        "tables": [1],
        "roles": [1],
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "clause" in exc_info.value.messages


def test_rls_post_schema_optional_fields(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "Test",
        "filter_type": "Regular",
        "tables": [1],
        "roles": [1],
        "clause": "id = 1",
        "description": "A description",
        "group_key": "department",
    }
    result = schema.load(data)
    assert result["description"] == "A description"
    assert result["group_key"] == "department"


def test_rls_post_schema_name_max_length(app_context: None) -> None:
    schema = RLSPostSchema()
    data = {
        "name": "x" * 256,
        "filter_type": "Regular",
        "tables": [1],
        "roles": [1],
        "clause": "id = 1",
    }
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert "name" in exc_info.value.messages


def test_rls_put_schema_partial_update(app_context: None) -> None:
    schema = RLSPutSchema()
    result = schema.load({"name": "Updated Name"})
    assert result["name"] == "Updated Name"


def test_rls_put_schema_empty_is_valid(app_context: None) -> None:
    schema = RLSPutSchema()
    result = schema.load({})
    assert result == {}


def test_rls_put_schema_rejects_invalid_filter_type(app_context: None) -> None:
    schema = RLSPutSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"filter_type": "BadType"})
    assert "filter_type" in exc_info.value.messages
