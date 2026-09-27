from note_taker.mongodb.config import mongoDB
from pymongo.operations import SearchIndexModel

def create_indexes():
    collection = mongoDB.db["embeddings"]

    collection.create_index("hash")
    collection.create_index("created_at")

    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 3072,
                    "similarity": "cosine",
                }
            ]
        },
        name="embedding_index",
        type="vectorSearch",
    )

    collection.create_search_index(model=search_index_model)

    print("MongoDB indexes created sucessfully")