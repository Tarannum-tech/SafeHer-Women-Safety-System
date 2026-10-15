# import os
# import sqlite3

# # Delete old database
# if os.path.exists("instance/safety.db"):
#     os.remove("instance/safety.db")
#     print("✅ Old database deleted")
# else:
#     print("No old database found")

# print("✅ Ready to create new database. Run python app.py")

import os

# Database file path
db_path = "instance/safety.db"

# Check if file exists
if os.path.exists(db_path):
    os.remove(db_path)
    print("✅ Database deleted successfully!")
else:
    print("❌ Database file not found!")

print("\nNow run: python app.py")