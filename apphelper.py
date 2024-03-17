import os
import datetime
from pymongo.mongo_client import MongoClient

class apphelper():
    def __init__(self):
        self.mongopass = (os.getenv("MONGO_PASS"))
        self.uri = f"mongodb+srv://bmattblake:{mongodb_pass}@cluster0.vk4vz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    def ping(self):
        # Create a new client and connect to the server
        self.client = MongoClient(uri)
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def db(self):
        self.db = client.MindGardenAI
        journal_entries = db.journal_entries
        return journal_entries

    def self(self):
        self.title = input()
        self.text = input()
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def entry(self):
        self.entry = journal_entries.insert_one({"title": self.title, "text": self.text, "time": self.time}).inserted_id
        return self.entry
    
    def display(self):
        print(self.entry)
    
    
apphelper()


