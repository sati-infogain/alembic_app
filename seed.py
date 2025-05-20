import datetime
from uuid import uuid4

from alembic_db import Flow, SessionLocal, User, user_flows


def seed():
    db = SessionLocal()
    try:
        # Create users
        user1 = User(id=uuid4(), name="Alice", email="alice@example.com")
        user2 = User(id=uuid4(), name="Bob", email="bob@example.com")

        # Create flows
        flow1 = Flow(id=uuid4(), name="Flow A", description="First flow")
        flow2 = Flow(id=uuid4(), name="Flow B", description="Second flow")

        db.add_all([user1, user2, flow1, flow2])
        db.commit()

        # Associate users and flows with permissions
        db.execute(
            user_flows.insert(),
            [
                {
                    "user_id": user1.id,
                    "flow_id": flow1.id,
                    "permission": "read",
                    "created_at": datetime.datetime.utcnow(),
                    "updated_at": datetime.datetime.utcnow(),
                },
                {
                    "user_id": user2.id,
                    "flow_id": flow1.id,
                    "permission": "write",
                    "created_at": datetime.datetime.utcnow(),
                    "updated_at": datetime.datetime.utcnow(),
                },
                {
                    "user_id": user2.id,
                    "flow_id": flow2.id,
                    "permission": "admin",
                    "created_at": datetime.datetime.utcnow(),
                    "updated_at": datetime.datetime.utcnow(),
                },
            ],
        )
        db.commit()
        print("Seed data inserted successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()