"""100人分のユーザーデータを作成するスクリプト"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import SessionLocal, engine, Base
from src.models.user import User


def seed_users(count: int = 100) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing_count = db.query(User).count()
        if existing_count > 0:
            db.query(User).delete()
            db.commit()

        users = [
            User(
                name=f"User {i:03d}",
                email=f"user{i:03d}@example.com",
            )
            for i in range(1, count + 1)
        ]

        db.add_all(users)
        db.commit()
        print(f"{count}件のユーザーを作成しました。")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
