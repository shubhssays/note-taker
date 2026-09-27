from bson import ObjectId
from pymongo.collection import Collection
from note_taker.mongodb.config import mongoDB
from note_taker.mongodb.embedding_model import Embedding


class EmbeddingRepository:

    def __init__(self):
        self.collection: Collection = mongoDB.db["embeddings"]


    def create(self, embedding: Embedding) -> Embedding:
        data = embedding.model_dump(
            exclude_none=True,
            by_alias=True
        )

        result = self.collection.insert_one(data)
        embedding.id = result.inserted_id
        return embedding


    def get_by(self, id: ObjectId | None, hash: str | None) -> Embedding | None:

        if id is not None and hash is not None:
            raise ValueError("Provide either id or hash, not both")

        if id is None and hash is None:
            raise ValueError("Provide either id or hash, anyone")

        condition = {}

        if id is not None:
            condition["id"] = id

        if hash is not None:
            condition["hash"] = hash

        embedding_document = self.collection.find_one(condition)

        if embedding_document is None:
            return None

        return Embedding.model_validate(embedding_document)


    def search_similar(self, query_embedding: list[float], limit: int = 100):
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "embedding_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "content": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    },
                }
            },
        ]

        return list(self.collection.aggregate(pipeline))



