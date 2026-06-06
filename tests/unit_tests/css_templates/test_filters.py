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

from unittest.mock import MagicMock

from superset.css_templates.filters import CssTemplateAllTextFilter


def test_css_template_all_text_filter_empty_value() -> None:
    mock_query = MagicMock()
    filter_instance = CssTemplateAllTextFilter("template_name", MagicMock())
    result = filter_instance.apply(mock_query, "")
    assert result is mock_query


def test_css_template_all_text_filter_none_value() -> None:
    mock_query = MagicMock()
    filter_instance = CssTemplateAllTextFilter("template_name", MagicMock())
    result = filter_instance.apply(mock_query, None)
    assert result is mock_query


def test_css_template_all_text_filter_with_value(app_context: None) -> None:
    mock_query = MagicMock()
    filter_instance = CssTemplateAllTextFilter("template_name", MagicMock())
    result = filter_instance.apply(mock_query, "my_template")
    mock_query.filter.assert_called_once()
    assert result is mock_query.filter.return_value
