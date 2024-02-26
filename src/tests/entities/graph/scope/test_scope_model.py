import uuid

import pytest

from src.entities.scope.models import Scope
from src.entities.scope.exceptions import ScopeAlreadyExistException


@pytest.mark.asyncio
class TestScopeModel:
    async def test_create_existing_scope(self, caplog):
        scope = Scope(
            id_=str(uuid.uuid4()),
            attr="scope",
        )
        await scope.create()
        with pytest.raises(
            ScopeAlreadyExistException,
            match=f"Scope {scope.id_} with name {scope.name} already exists",
        ):
            scope_copy = Scope(
                id_=scope.id_,
                attr=scope.name,
            )
            await scope_copy.create()
