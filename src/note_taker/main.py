from note_taker.mongodb.config import mongoDB
from note_taker.mongodb.indexes import create_indexes
from note_taker.utils.telegram import poll_telegram


def main():

    # connect mongodb first
    mongoDB.connect()

    # creating mongodb indexing if not exists
    create_indexes()

    # Poll the telegram for new messages
    poll_telegram()


if __name__ == "__main__":
    main()