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
"""Generic base commands for adding/removing favorites.

Subclasses only need to set class-level attributes to configure the DAO,
exception classes, and error handling for their specific model type.
"""

from __future__ import annotations

import logging
from functools import partial
from typing import Any, ClassVar

from superset.commands.base import BaseCommand
from superset.commands.exceptions import CommandException
from superset.daos.favorites import FavoritesMixin
from superset.utils.decorators import on_error, transaction

logger = logging.getLogger(__name__)


class BaseAddFavoriteCommand(BaseCommand):
    """Generic command to add a model instance to the user's favorites.

    Subclasses must define:
        dao: A DAO class that extends FavoritesMixin and provides ``find_by_id``.
        not_found_error: Exception to raise when the model is not found.
        access_denied_error: Exception to raise on access denial (optional).
        fave_error: Exception to wrap transaction failures.
    """

    dao: ClassVar[type[FavoritesMixin]]
    not_found_error: ClassVar[type[CommandException]]
    access_denied_error: ClassVar[type[CommandException] | None] = None
    fave_error: ClassVar[type[CommandException]]

    def __init__(self, model_id: int) -> None:
        self._model_id = model_id
        self._model: Any = None

    def run(self) -> None:
        @transaction(on_error=partial(on_error, reraise=self.fave_error))
        def _run() -> None:
            self.validate()
            if self._model:
                self.dao.add_favorite(self._model)

        _run()

    def validate(self) -> None:
        model = self.dao.find_by_id(self._model_id)  # type: ignore[attr-defined]
        if not model:
            raise self.not_found_error()
        self._check_access(model)
        self._model = model

    def _check_access(self, model: Any) -> None:
        """Override in subclasses to add access control checks."""


class BaseDelFavoriteCommand(BaseCommand):
    """Generic command to remove a model instance from the user's favorites.

    Subclasses must define:
        dao: A DAO class that extends FavoritesMixin and provides ``find_by_id``.
        not_found_error: Exception to raise when the model is not found.
        access_denied_error: Exception to raise on access denial (optional).
        unfave_error: Exception to wrap transaction failures.
    """

    dao: ClassVar[type[FavoritesMixin]]
    not_found_error: ClassVar[type[CommandException]]
    access_denied_error: ClassVar[type[CommandException] | None] = None
    unfave_error: ClassVar[type[CommandException]]

    def __init__(self, model_id: int) -> None:
        self._model_id = model_id
        self._model: Any = None

    def run(self) -> None:
        @transaction(on_error=partial(on_error, reraise=self.unfave_error))
        def _run() -> None:
            self.validate()
            if self._model:
                self.dao.remove_favorite(self._model)

        _run()

    def validate(self) -> None:
        model = self.dao.find_by_id(self._model_id)  # type: ignore[attr-defined]
        if not model:
            raise self.not_found_error()
        self._check_access(model)
        self._model = model

    def _check_access(self, model: Any) -> None:
        """Override in subclasses to add access control checks."""
