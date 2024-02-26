import uuid

import pytest

from src.entities.resource.models import Resource
from src.entities.resource.exceptions import ResourceAlreadyExistException


@pytest.mark.asyncio
class TestResourceModel:
    async def test_create_existing_resource(self, caplog):
        resource = Resource(
            id_=str(uuid.uuid4()),
            attr="resource",
        )
        await resource.create()
        with pytest.raises(
            ResourceAlreadyExistException,
            match=f"Resource {resource.id_} with type {resource.type} already exists",
        ):
            resource_copy = Resource(
                id_=resource.id_,
                attr=resource.type,
            )
            await resource_copy.create()
