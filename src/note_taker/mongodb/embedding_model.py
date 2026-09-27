from datetime import datetime, timezone

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

class Embedding(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId | None = Field(default=None, alias="_id")
    hash: str
    content: str
    embedding: list[float] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Embedding id={self.id} hash={self.hash} content={self.content} embedding={self.embedding[:5]} created_at={self.created_at}>"
