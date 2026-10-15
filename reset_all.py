import os
import time

print("="*50)
print("Resetting SafeHer Database")
print("="*50)

# Close any existing connections
time.sleep(2)

# Delete database file
db_path = "instance/safety.db"
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("✅ Database deleted successfully")
    except PermissionError:
        print("❌ Database file is locked. Please close all terminal windows and try again.")
        print("   Steps:")
        print("   1. Close this terminal")
        print("   2. Open new terminal")
        print("   3. Run: python app.py")
        exit(1)
else:
    print("No database file found")

print("\n✅ Ready to create new database.")
print("Run: python app.py")