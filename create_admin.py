from app import app, db
from models import User

# Set the details for the admin user
username = "mitadmin"
prn = "123456"
password = "mitadmin"

with app.app_context():
    # Create the admin user
    admin_user = User(username=username, prn=prn, is_admin=True)
    admin_user.set_password(password)
    db.session.add(admin_user)
    db.session.commit()

    # Verify the admin user
    admin = User.query.filter_by(username="mitadmin").first()
    print(admin)          # This should print the details of the admin user
    print(admin.is_admin) # This should print True
