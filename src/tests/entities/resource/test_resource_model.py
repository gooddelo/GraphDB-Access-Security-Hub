import uuid

import pytest

from src.entities.resource.models import Resource


@pytest.mark.asyncio
class TestResourceModel:
    async def test_create_existing_resource(self, caplog):
        resource = Resource(
            resource_id=uuid.uuid4(),
            type="resource",
        )
        await resource.create()
        with pytest.raises(ValueError, match=f"Resource {resource.resource_id} with type {resource.type} already exists"):
            resource_copy = Resource(
                resource_id=resource.resource_id,
                type=resource.type,
            )
            await resource_copy.create()