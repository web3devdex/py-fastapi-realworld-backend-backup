from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlmodel.ext.asyncio.session import AsyncSession

from conduit.domain.dtos.tag import CreateTagDTO, TagDTO
from conduit.domain.mapper import IModelMapper
from conduit.domain.repositories.tag import ITagRepository
from conduit.infrastructure.models import Tag


class TagRepository(ITagRepository):
    """Repository for Tag model."""

    def __init__(self, tag_mapper: IModelMapper[Tag, TagDTO]):
        self._tag_mapper = tag_mapper

    async def create(self, session: AsyncSession, tags: Sequence[CreateTagDTO]) -> None:
        query = (
            insert(Tag)
            .on_conflict_do_nothing()
            .values([{"tag": tag.tag, "created_at": datetime.now()} for tag in tags])
        )
        await session.execute(query)

    async def get_all(self, session: AsyncSession) -> list[TagDTO]:
        query = select(Tag)
        tags = await session.scalars(query)
        return [self._tag_mapper.to_dto(tag) for tag in tags]
