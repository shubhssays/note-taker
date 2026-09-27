import time
import requests

from note_taker.constants.enums import EVENT_TYPE, MESSAGE_IDENTIFIER
from note_taker.mongodb.embedding_model import Embedding
from note_taker.mongodb.embedding_repository import EmbeddingRepository
from note_taker.utils.hashing import hash_text
from note_taker.utils.settings import settings
from note_taker.utils.event_emitter import EventEmitter
from note_taker.utils.gemini_embeddings import generate_embeddings

emitter = EventEmitter()
repo = EmbeddingRepository()

THRESHOLD = 0.7

def poll_telegram():
    offset = 0

    while True:
        response = requests.get(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates",
            params={
                "offset": offset,
                "limit": 100,
                "timeout": 30,
            },
            timeout=35,
        )

        response.raise_for_status()

        updates = response.json()["result"]

        for update in updates:
            message = update.get("message", {})

            emitter.emit(EVENT_TYPE.MESSAGE_RECEIVED, message)

            # Next request starts after this update
            offset = update["update_id"] + 1

        time.sleep(1)

def send_telegram_message(chat_id: int, text: str):
    response = requests.post(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
        },
    )

    response.raise_for_status()
    return response.json()

@emitter.on(EVENT_TYPE.MESSAGE_RECEIVED)
def message_processing(message: dict):
    # photos = message.get("photo", [])
    """We will ignore images for now"""

    chat = message.get("chat", None)

    exact_message = message.get("text", None)
    exact_message = exact_message.strip()

    """This is to query"""
    if exact_message.casefold().startswith(MESSAGE_IDENTIFIER.QUERY.casefold()):
        search_message(exact_message, chat)
    else:
        """This is to save the content"""
        add_message(exact_message)


def search_message(message: str, chat: dict | None):
    message = message.replace(MESSAGE_IDENTIFIER.QUERY, "")

    """Vectorized the message"""
    query_embedding = generate_embeddings(message)

    """Fetching the matching message"""
    matching_messages = repo.search_similar(query_embedding)

    if matching_messages:
        """Chunking it so that we don't end up violating message length of telegram"""
        messages = []

        for message in matching_messages:
            if message.get("content") and message.get("score") >= THRESHOLD:
               messages.extend(split_message(message.get("content")))

        if not messages:
            no_message_found = "No matching message found"
            send_telegram_message(chat.get("id", 0), no_message_found)
            print(no_message_found)

        """Sending each matching as separate message and pausing in between for 1 second"""
        for msg in messages:
            send_telegram_message(chat.get("id", 0), msg)
            time.sleep(1)

        print("Message sent successfully of length", len(messages))

    else:
        no_message_found = "No matching message found"
        send_telegram_message(chat.get("id", 0), no_message_found)
        print(no_message_found)


def add_message(message: str):
    """Check if message has already exist"""
    message_hash = hash_text(message)
    message_exist = repo.get_by(None, message_hash)

    if not message_exist:
        """Vectorized the message"""
        vector_embeddings = generate_embeddings(message)

        """Store the message"""
        embedding = Embedding(
            hash=message_hash,
            content=message,
            embedding=vector_embeddings
        )
        result = repo.create(embedding)
        print("Message saved to mongodb", result.get("id"))
    else:
        print("duplicate message found", message)


def split_message(text: str, max_length: int = 4000):
    chunks = []

    while len(text) > max_length:
        split_at = text.rfind(" ", 0, max_length)

        if split_at == -1:
            # No space found — unavoidable hard split
            split_at = max_length

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()

    if text:
        chunks.append(text)

    return chunks















