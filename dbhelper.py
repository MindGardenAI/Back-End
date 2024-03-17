import os
import datetime
from pymongo.mongo_client import MongoClient

class dbhelper():
    def __init__(self):          
        mongodb_pass = (os.getenv("MONGO_PASS"))
        mongodb_pass = "Kbt070322MDB"
        uri = f"mongodb+srv://bmattblake:{mongodb_pass}@cluster0.vk4vz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        # Create a new client and connect to the server
        client = MongoClient(uri)
            
        self.db = client.MindGardenAI
        self.journal_entries = self.db.journal_entries
    
    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def add_entry(self, title, text):
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry_id = self.journal_entries.insert_one({"title": title, "time": curr_time, "text": text}).inserted_id
        return entry_id

    def get_entries(self):
        entries = list()
        for entry in self.journal_entries.find():
            entries.append(entry)
        return entries
    
    def get_user_entries(self, user_id):
        entries = list()
        for entry in self.journal_entries.find({"uid": user_id}):
            entries.append(entry)
        return entries
    
    


