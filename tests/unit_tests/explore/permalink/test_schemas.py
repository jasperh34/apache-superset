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

from superset.explore.permalink.schemas import (
    ExplorePermalinkSchema,
    ExplorePermalinkStateSchema,
)


def test_permalink_state_schema_valid_minimal() -> None:
    schema = ExplorePermalinkStateSchema()
    result = schema.load({"formData": {"viz_type": "bar"}})
    assert result["formData"] == {"viz_type": "bar"}


def test_permalink_state_schema_with_url_params() -> None:
    schema = ExplorePermalinkStateSchema()
    result = schema.load(
        {
            "formData": {},
            "urlParams": [("key1", "val1"), ("key2", "val2")],
        }
    )
    assert result["urlParams"] == [("key1", "val1"), ("key2", "val2")]


def test_permalink_state_schema_with_chart_state() -> None:
    schema = ExplorePermalinkStateSchema()
    result = schema.load(
        {
            "formData": {},
            "chartState": {"sortBy": "col1"},
        }
    )
    assert result["chartState"] == {"sortBy": "col1"}


def test_permalink_state_schema_rejects_missing_form_data() -> None:
    schema = ExplorePermalinkStateSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({})
    assert "formData" in exc_info.value.messages


def test_permalink_state_schema_rejects_none_form_data() -> None:
    schema = ExplorePermalinkStateSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"formData": None})
    assert "formData" in exc_info.value.messages


def test_permalink_schema_valid_minimal() -> None:
    schema = ExplorePermalinkSchema()
    result = schema.load(
        {
            "datasourceType": "table",
            "state": {"formData": {}},
        }
    )
    assert result["datasourceType"] == "table"


def test_permalink_schema_with_all_fields() -> None:
    schema = ExplorePermalinkSchema()
    result = schema.load(
        {
            "chartId": 5,
            "datasourceType": "table",
            "datasourceId": 10,
            "datasource": "10__table",
            "state": {"formData": {"viz_type": "line"}},
        }
    )
    assert result["chartId"] == 5
    assert result["datasourceId"] == 10
    assert result["datasource"] == "10__table"


def test_permalink_schema_rejects_missing_datasource_type() -> None:
    schema = ExplorePermalinkSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load({"state": {"formData": {}}})
    assert "datasourceType" in exc_info.value.messages


def test_permalink_schema_optional_chart_id() -> None:
    schema = ExplorePermalinkSchema()
    result = schema.load(
        {
            "datasourceType": "dataset",
            "state": {"formData": {}},
        }
    )
    assert "chartId" not in result


def test_permalink_schema_nullable_chart_id() -> None:
    schema = ExplorePermalinkSchema()
    result = schema.load(
        {
            "chartId": None,
            "datasourceType": "table",
            "state": {"formData": {}},
        }
    )
    assert result["chartId"] is None
