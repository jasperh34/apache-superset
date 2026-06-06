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

from superset.explore.form_data.schemas import FormDataPostSchema, FormDataPutSchema


def test_form_data_post_schema_valid() -> None:
    schema = FormDataPostSchema()
    result = schema.load(
        {
            "datasource_id": 1,
            "datasource_type": "table",
            "form_data": '{"viz_type": "bar"}',
        }
    )
    assert result["datasource_id"] == 1
    assert result["datasource_type"] == "table"
    assert result["form_data"] == '{"viz_type": "bar"}'


def test_form_data_post_schema_with_chart_id() -> None:
    schema = FormDataPostSchema()
    result = schema.load(
        {
            "datasource_id": 1,
            "datasource_type": "table",
            "form_data": "{}",
            "chart_id": 42,
        }
    )
    assert result["chart_id"] == 42


def test_form_data_post_schema_rejects_missing_datasource_id() -> None:
    schema = FormDataPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "datasource_type": "table",
                "form_data": "{}",
            }
        )
    assert "datasource_id" in exc_info.value.messages


def test_form_data_post_schema_rejects_missing_datasource_type() -> None:
    schema = FormDataPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "datasource_id": 1,
                "form_data": "{}",
            }
        )
    assert "datasource_type" in exc_info.value.messages


def test_form_data_post_schema_rejects_invalid_datasource_type() -> None:
    schema = FormDataPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "datasource_id": 1,
                "datasource_type": "invalid",
                "form_data": "{}",
            }
        )
    assert "datasource_type" in exc_info.value.messages


def test_form_data_post_schema_rejects_missing_form_data() -> None:
    schema = FormDataPostSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "datasource_id": 1,
                "datasource_type": "table",
            }
        )
    assert "form_data" in exc_info.value.messages


def test_form_data_post_schema_valid_datasource_types() -> None:
    schema = FormDataPostSchema()
    for ds_type in ("table", "dataset", "query", "saved_query", "view"):
        result = schema.load(
            {
                "datasource_id": 1,
                "datasource_type": ds_type,
                "form_data": "{}",
            }
        )
        assert result["datasource_type"] == ds_type


def test_form_data_put_schema_valid() -> None:
    schema = FormDataPutSchema()
    result = schema.load(
        {
            "datasource_id": 2,
            "datasource_type": "dataset",
            "form_data": '{"key": "val"}',
        }
    )
    assert result["datasource_id"] == 2


def test_form_data_put_schema_rejects_invalid_datasource_type() -> None:
    schema = FormDataPutSchema()
    with pytest.raises(ValidationError) as exc_info:
        schema.load(
            {
                "datasource_id": 1,
                "datasource_type": "bad_type",
                "form_data": "{}",
            }
        )
    assert "datasource_type" in exc_info.value.messages
