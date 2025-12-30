# app/utils/db_utils.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_or_create(session: AsyncSession, model, **kwargs):
    """
    Mimics Django's `Model.objects.get_or_create`.

    Returns:
        (instance, created) - `created` is True if a new row was inserted.
    """
    stmt = select(model).filter_by(**kwargs)
    result = await session.execute(stmt)
    instance = result.scalar_one_or_none()

    if instance:
        return instance, False

    # Create and flush so we get an ID
    instance = model(**kwargs)
    session.add(instance)
    await session.flush()          # assigns PK without committing
    return instance, True
