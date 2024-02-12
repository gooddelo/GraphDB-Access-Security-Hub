import uuid

import pytest

from src.entities.scope.models import Scope


@pytest.mark.asyncio
class TestScopeModel:
    async def test_create_existing_scope(self, caplog):
        scope = Scope(
            scope_id=uuid.uuid4(),
            name="scope",
        )
        await scope.create()
        with pytest.raises(ValueError, match=f"Scope {scope.scope_id} with name {scope.name} already exists"):
            scope_copy = Scope(
                scope_id=scope.scope_id,
                name=scope.name,
            )
            await scope_copy.create()