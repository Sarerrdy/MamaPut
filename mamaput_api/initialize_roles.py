# initialize_roles.py
from models.role import Role
from models.user import User
from models.user_role import UserRole
from database import db


# def initialize_roles():
def populate_roles():
    roles = ['User', 'Admin', 'RestaurantManager', 'Shipper']
    for role_name in roles:
        role = Role(role_name=role_name)
        role.save()


# def assign_default_admin():
#     admin_user = User.query.filter_by(email='mamaputwebapp@gmail.com').first()
#     if admin_user:
#         admin_role = Role.query.filter_by(role_name='Admin').first()
#         if admin_role:
#             user_role = UserRole(user_id=admin_user.user_id,
#                                  role_id=admin_role.role_id)
#             user_role.save()


if __name__ == "__main__":
    # db.create_all()  # Ensure all tables are created
    # initialize_roles()
    # assign_default_admin()
    with db.session.begin():
        populate_roles()
        print("Roles have been added to the database.")
