import os
import datetime
from pymongo.mongo_client import MongoClient


class dbhelper():
    def __init__(self):          
        mongodb_pass = (os.getenv("MONGO_PASS"))
        mongodb_pass = "Kbt070322MDB"
        uri = f"mongodb+srv://bmattblake:{mongodb_pass}@cluster0.vk4vz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        

        # Create a new client and connect to the server
        self.client = MongoClient(uri, maxIdleTimeMS=60000, connect=False)
            
        self.db = self.client.MindGardenAI
        self.journal_entries = self.db.journal_entries
        self.goals = self.db.goals
    
    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def add_entry(self, uid, body):
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry_id = self.journal_entries.insert_one({"uid": uid, "time": curr_time, "body": body}).inserted_id
        return entry_id
    
    '''def add_entry(self,uid, title, text):
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry_id = self.journal_entries.insert_one({"uid": uid, "title": title, "time": curr_time, "text": text}).inserted_id
        return entry_id'''

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
    
    
    def get_todays_entries(self, user_id):
        entries = list()
        for entry in self.journal_entries.find({"uid": user_id}):
            entry_date_str = entry["time"]
            entry_date = datetime.datetime.strptime(entry_date_str, '%Y-%m-%d %H:%M:%S')
            entry_day = entry_date.date()

            today = datetime.datetime.today().strftime("%Y-%m-%d")
            if str(entry_day) == today:
                entries.append(entry)
        return entries
    
    def add_goal(self, user_id, title, content):
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry_id = self.goals.insert_one({"uid": user_id, "title": title, "create_data": curr_time, "content": content}).inserted_id
        return str(entry_id)
    
    def get_user_goals(self, user_id):
        goals = list()
        for goal in self.goals.find({"uid": user_id}):
            goals.append(goal)
        return goals


