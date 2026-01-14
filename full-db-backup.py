import os
import pymongo
from datetime import datetime
from bson import json_util
import requests


def get_human_size(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    if size_mb >= 1024:
        return f"{size_mb / 1024:.2f} GB"
    return f"{size_mb:.2f} MB"


def get_directory_size(path):
    total_size = 0
    for root, _, files in os.walk(path):
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))
    return total_size


def dump_full_database(host, port, username, password, database, backup_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_backup_dir = os.path.join(backup_dir, f"{database}_full_dump_{timestamp}")
    os.makedirs(db_backup_dir, exist_ok=True)

    try:
        client = pymongo.MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}/",
            serverSelectionTimeoutMS=5000
        )

        db = client[database]
        collections = db.list_collection_names()

        if not collections:
            raise Exception("No collections found in database")

        for collection_name in collections:
            collection = db[collection_name]
            backup_file = os.path.join(db_backup_dir, f"{collection_name}.json")

            with open(backup_file, "w", encoding="utf-8") as f:
                f.write("[\n")
                first = True
                for doc in collection.find():
                    if not first:
                        f.write(",\n")
                    f.write(json_util.dumps(doc, indent=4))
                    first = False
                f.write("\n]")

            print(f"✅ Dumped collection: {collection_name}")

        client.close()

        total_size = get_directory_size(db_backup_dir)
        readable_size = get_human_size(total_size)

        notify_discord(
            DISCORD_WEBHOOK_URL,
            f"✅ **MongoDB Full Database Backup Completed**\n"
            f"🗄 Database: `{database}`\n"
            f"📚 Collections: `{len(collections)}`\n"
            f"📦 Total Size: **{readable_size}**\n"
            f"📂 Path: `{db_backup_dir}`"
        )

        return db_backup_dir

    except Exception as e:
        notify_discord(
            DISCORD_WEBHOOK_URL,
            f"❌ **MongoDB Full Database Backup Failed**\n"
            f"🗄 Database: `{database}`\n"
            f"⚠️ Error: `{str(e)}`"
        )
        return None


def notify_discord(webhook_url, message):
    try:
        response = requests.post(webhook_url, json={"content": message}, timeout=5)
        if response.status_code == 204:
            print("✅ Discord notification sent")
        else:
            print(f"⚠️ Discord response code: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord notification failed: {e}")


if __name__ == "__main__":

    HOST = "172.****"
    PORT = 27017
    USERNAME = "backup_user"
    PASSWORD = "********"
    DATABASE = "my-db"
    BACKUP_DIR = "/root/mongo-backup"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/13*********"

    dump_full_database(
        HOST,
        PORT,
        USERNAME,
        PASSWORD,
        DATABASE,
        BACKUP_DIR
    )
