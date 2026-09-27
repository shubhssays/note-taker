from google import genai
from note_taker.utils.settings import settings


def generate_embeddings(contents: str, model="gemini-embedding-001"):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    result = client.models.embed_content(
        model=model,
        contents=contents
    )

    embedding = result.embeddings[0].values
    return embedding
