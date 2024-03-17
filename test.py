from dbhelper import dbhelper
import uuid

helper = dbhelper()
user_id = str(uuid.uuid4())

print(helper.add_entry(user_id, "Monday", "I hate mondays"))

#print(helper.get_entries())

print(helper.get_user_entries(user_id))
