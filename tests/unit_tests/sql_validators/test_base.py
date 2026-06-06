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

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from superset.sql_validators.base import BaseSQLValidator, SQLValidationAnnotation


def test_sql_validation_annotation_to_dict() -> None:
    annotation = SQLValidationAnnotation(
        message="Syntax error near SELECT",
        line_number=1,
        start_column=5,
        end_column=10,
    )
    result = annotation.to_dict()
    assert result == {
        "line_number": 1,
        "start_column": 5,
        "end_column": 10,
        "message": "Syntax error near SELECT",
    }


def test_sql_validation_annotation_to_dict_with_none_values() -> None:
    annotation = SQLValidationAnnotation(
        message="General error",
        line_number=None,
        start_column=None,
        end_column=None,
    )
    result = annotation.to_dict()
    assert result == {
        "line_number": None,
        "start_column": None,
        "end_column": None,
        "message": "General error",
    }


def test_sql_validation_annotation_attributes() -> None:
    annotation = SQLValidationAnnotation(
        message="msg",
        line_number=3,
        start_column=1,
        end_column=7,
    )
    assert annotation.message == "msg"
    assert annotation.line_number == 3
    assert annotation.start_column == 1
    assert annotation.end_column == 7


def test_base_sql_validator_name() -> None:
    assert BaseSQLValidator.name == "BaseSQLValidator"


def test_base_sql_validator_validate_raises_not_implemented() -> None:
    mock_database = MagicMock()
    with pytest.raises(NotImplementedError):
        BaseSQLValidator.validate(
            sql="SELECT 1",
            catalog=None,
            schema=None,
            database=mock_database,
        )
