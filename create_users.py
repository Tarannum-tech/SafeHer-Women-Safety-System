from app import app, db, User, GuardianRelation
from werkzeug.security import generate_password_hash

with app.app_context():
    # Delete all existing users (except admin)
    User.query.filter(User.username != 'admin').delete()
    GuardianRelation.query.delete()
    db.session.commit()
    
    # Create Maniya (User)
    maniya = User(
        username='maniya',
        email='maniya@test.com',
        full_name='Maniya',
        phone='9876543210',
        role='user',
        is_verified=True,
        password_hash=generate_password_hash('maniya123')
    )
    db.session.add(maniya)
    print("✅ Created user: maniya (password: maniya123)")
    
    # Create Maniya Parents (Guardian)
    parents = User(
        username='maniya-parents',
        email='parents@test.com',
        full_name='Maniya Parents',
        phone='9876543211',
        role='guardian',
        is_verified=True,
        password_hash=generate_password_hash('parents123')
    )
    db.session.add(parents)
    print("✅ Created guardian: maniya-parents (password: parents123)")
    
    db.session.commit()
    
    # Create guardian relation
    relation = GuardianRelation(
        user_id=maniya.id,
        guardian_id=parents.id,
        relationship='Parents'
    )
    db.session.add(relation)
    db.session.commit()
    print("✅ Guardian relation created: Maniya -> Maniya Parents")
    
    print("\n" + "="*50)
    print("Test Credentials:")
    print("="*50)
    print("User: maniya / maniya123")
    print("Guardian: maniya-parents / parents123")
    print("Admin: admin / admin123")
    print("="*50)