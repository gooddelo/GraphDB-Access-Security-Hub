import uuid

from faststream.rabbit import RabbitBroker

from src.api.amqp import api_router
from src.config.amqp import AMQP_CONFIG, GASH_EXCHANGE
from src.api.amqp.v1.queues import (
    ScopeQueuesV1,
    ResourceQueuesV1,
    UserQueuesV1,
    PermitQueuesV1,
)
AMQP_CONFIG.host = 'localhost'
broker = RabbitBroker(AMQP_CONFIG.connection_url())
broker.include_routers(api_router)


async def main():
    async with broker:
        owner_data = {
            "id_": str(uuid.uuid4()),
            "role": "owner",
            "resources": [],
            "belong_scopes": [],
        }
        company_data = {
            "id_": str(uuid.uuid4()),
            "name": "company",
            "owner": {
                "id_": owner_data["id_"],
                "role": owner_data["role"],
            },
            "users": [],
            "scopes": [],
            "resources": [],
        }
        selling_point_data = {
            "id_": str(uuid.uuid4()),
            "name": "selling_point",
            "owner": {
                "id_": owner_data["id_"],
                "role": owner_data["role"],
            },
            "users": [],
            "scopes": [],
            "resources": [],
        }
        company_update_data = {
            "id_": company_data["id_"],
            "old_name": "company",
            "new_scopes": [
                {
                    "id_": selling_point_data["id_"],
                    "name": selling_point_data["name"],
                }
            ]
        }
        company_resource_data = {
            "id_": str(uuid.uuid4()),
            "type": "company_resource",
            "users": [],
            "scopes": [
                {
                    "id_": company_data["id_"],
                    "name": "company",
                }
            ],   
        }
        employee_data = {
            "id_": str(uuid.uuid4()),
            "role": "empoyee",
            "resources": [],
            "belong_scopes": [
                {
                    "id_": company_data["id_"],
                    "name": company_data["name"],
                }
            ],
        }
        false_permit_request_data = {
            "subject": {
                "id_": employee_data["id_"],
                "role": employee_data["role"],
            },
            "object": {
                "id_": company_resource_data["id_"],
                "type": company_resource_data["type"],
            },
            "action": "read",
        }
        true_permit_request_data = {
            "subject": {
                "id_": owner_data["id_"],
                "role": owner_data["role"],
            },
            "object": {
                "id_": company_resource_data["id_"],
                "type": company_resource_data["type"],
            },
            "action": "read",
        }
        await broker.publish(
            message=owner_data,
            queue=UserQueuesV1.CREATE,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        await broker.publish(
            message=company_data,
            queue=ScopeQueuesV1.CREATE,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        await broker.publish(
            message=selling_point_data,
            queue=ScopeQueuesV1.CREATE,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        await broker.publish(
            message=company_update_data,
            queue=ScopeQueuesV1.UPDATE,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        await broker.publish(
            message=company_resource_data,
            queue=ResourceQueuesV1.CREATE,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        await broker.publish(
            message=employee_data,
            queue=UserQueuesV1.CREATE,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        permit_false = await broker.publish(
            message=false_permit_request_data,
            queue=PermitQueuesV1.GET,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        print(f"{permit_false = }")
        permit_true = await broker.publish(
            message=true_permit_request_data,
            queue=PermitQueuesV1.GET,
            exchange=GASH_EXCHANGE,
            rpc=True,
        )
        print(f"{permit_true = }")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())