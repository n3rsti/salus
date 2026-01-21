from sqlmodel import Session, select
from api.database import engine
from api.models.enums import Role
from api.models.user_models import Users
from api.security.crypto import hash_password


def create_super_admin(username: str, email: str, password: str):
    with Session(engine) as session:
        admin_user = Users(
            username=username,
            email=email,
            role_id=Role.SUPER_ADMIN,
            password=hash_password(password),
        )
        session.add(admin_user)
        session.commit()


if __name__ == "__main__":
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    password_repeat = input("Repeat password: ")
    if password != password_repeat:
        print("Passwords do not match")
        exit(1)

    create_super_admin(username, email, password)
