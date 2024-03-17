from dbhelper import dbhelper
import uuid

helper = dbhelper()
user_id = str(uuid.uuid4())
user_id = "cf1b9ab0-bb76-497f-85ea-77a80dc565f1"
#print(helper.add_entry(user_id, "Wendnesday", "Hump DAYYY"))

#print(helper.get_entries())

print(helper.get_todays_entries("cf1b9ab0-bb76-497f-85ea-77a80dc565f1"))

helper.ping()
