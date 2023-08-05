import autodynatrace
import time
import datetime

from pymongo import MongoClient

client = MongoClient(host="192.168.15.101")


def send_request():
    db = client.test_database
    post = {
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow(),
    }

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print("Post ID", post_id)


@autodynatrace.trace
def main():
    time.sleep(1)
    send_request()
    time.sleep(60)


if __name__ == "__main__":
    main()
