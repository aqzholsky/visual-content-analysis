from motor.motor_asyncio import AsyncIOMotorClient


async def get_analysis_by_request_id(
    conn: AsyncIOMotorClient,
    request_id: str,
) -> dict:
    return await conn["analysis"]["analysis_results"].find_one(
        {"request_id": request_id}, {"_id": 0}
    )


async def insert_analysis_result(conn: AsyncIOMotorClient, content: dict) -> dict:
    return await conn["analysis"]["analysis_results"].insert_one(content)


async def delete_analysis_result(conn: AsyncIOMotorClient, request_id: str) -> dict:
    return await conn["analysis"]["analysis_results"].delete_one(
        {"request_id": request_id}
    )


async def is_analysis_exists(conn: AsyncIOMotorClient, request_id: str) -> bool:
    return (
        await conn["analysis"]["analysis_results"].count_documents(
            {"request_id": request_id}
        )
        > 0
    )
