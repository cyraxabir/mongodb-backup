import os
import json
import pymongo
from datetime import datetime
from bson import json_util
import requests


def get_file_size(file_path):
    """
    Returns human-readable file size (MB / GB)
    """
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)

    if size_mb >= 1024:
        return f"{size_mb / 1024:.2f} GB"
    return f"{size_mb:.2f} MB"


def dump_mongodb_collection(host, port, username, password, database, collection, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{collection}_dump_{timestamp}.json")

    try:
        client = pymongo.MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}/",
            serverSelectionTimeoutMS=5000
        )
        db = client[database]
        col = db[collection]

        with open(backup_file, "w", encoding="utf-8") as f:
            f.write("[\n")

            first_doc = True
            for doc in col.find():
                if not first_doc:
                    f.write(",\n")
                f.write(json_util.dumps(doc, indent=4))
                first_doc = False

            f.write("\n]")

        client.close()

        backup_size = get_file_size(backup_file)

        print(f"✅ Dump successful: {backup_file} ({backup_size})")

        notify_discord(
            DISCORD_WEBHOOK_URL,
            f"✅ **Mutation MongoDB Backup Completed**\n"
            f"📁 Collection: `{collection}`\n"
            f"📦 File Size: **{backup_size}**\n"
            f"🕒 Time: `{timestamp}`"
        )

        return backup_file

    except Exception as e:
        print(f"❌ Dump failed: {e}")
        notify_discord(
            DISCORD_WEBHOOK_URL,
            f"❌ **Mutation MongoDB Backup Failed**\n"
            f"⚠️ Error: `{str(e)}`"
        )
        return None


def notify_discord(webhook_url, message):
    data = {
        "content": message
    }
    try:
        response = requests.post(webhook_url, json=data, timeout=5)
        if response.status_code == 204:
            print("✅ Discord notification sent.")
        else:
            print(f"⚠️ Discord webhook responded with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to send Discord notification: {e}")


if __name__ == "__main__":

    HOST = "172.****"
    PORT = 27017
    USERNAME = "backup_user"
    PASSWORD = "********"
    DATABASE = "my-db"
    COLLECTION = "drafts"
    BACKUP_DIR = "/root/mongo-backup"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/13*********"

    dump_mongodb_collection(
        HOST,
        PORT,
        USERNAME,
        PASSWORD,
        DATABASE,
        COLLECTION,
        BACKUP_DIR
    )
