from app import app, db, User
from werkzeug.security import generate_password_hash
import os

print("=" * 50)
print("Creating Test Users")
print("=" * 50)

# Check if database exists
if not os.path.exists("instance/safety.db"):
    print("Creating new database...")
    with app.app_context():
        db.create_all()
        print("✅ Database created")

with app.app_context():
    # Create test users
    users = [
        {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test123',
            'full_name': 'Test User',
            'phone': '9876543210',
            'role': 'user'
        },
        {
            'username': 'testguardian',
            'email': 'guardian@example.com',
            'password': 'guardian123',
            'full_name': 'Test Guardian',
            'phone': '9876543211',
            'role': 'guardian'
        }
    ]
    
    print("\nCreating test users:")
    for user_data in users:
        existing = User.query.filter_by(username=user_data['username']).first()
        if not existing:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                phone=user_data['phone'],
                role=user_data['role'],
                password_hash=generate_password_hash(user_data['password'])
            )
            db.session.add(user)
            print(f"  ✅ Created: {user_data['username']} (password: {user_data['password']})")
        else:
            print(f"  ⚠️ Already exists: {user_data['username']}")
    
    db.session.commit()
    
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@safety.com',
            full_name='System Administrator',
            phone='0000000000',
            role='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print(f"  ✅ Created: admin (password: admin123)")
    else:
        print(f"  ⚠️ Already exists: admin")

print("\n" + "-" * 50)
print("Test Users Summary:")
print("-" * 50)
print("  User:      testuser / test123")
print("  Guardian:  testguardian / guardian123")
print("  Admin:     admin / admin123")
print("\n" + "=" * 50)
print("✅ Test users created successfully!")
print("=" * 50)