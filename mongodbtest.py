import os
import datetime
from pymongo.mongo_client import MongoClient

mongodb_pass = (os.getenv("MONGO_PASS"))
mongodb_pass = "Kbt070322MDB"
uri = f"mongodb+srv://bmattblake:{mongodb_pass}@cluster0.vk4vz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.MindGardenAI
journal_entries = db.journal_entries


curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
entry_id = journal_entries.insert_one({"title": "My Thoughts", "time": curr_time, "text": "Today I ate an orange."}).inserted_id
print(entry_id)