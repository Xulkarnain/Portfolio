from sqlalchemy import select

from app.database.session import SessionLocal
from app.models import Post, User


with SessionLocal() as session:
    posts = session.scalars(
        select(Post)
    ).all()

    print("Post → Owner:\n")

    for post in posts:
        print(f"Post: {post.title}")
        print(f"Source: {post.source}")
        print(f"Owner: {post.owner.full_name}")
        print()

    users = session.scalars(
        select(User)
    ).all()

    print("User → Posts:\n")

    for user in users:
        print(f"User: {user.full_name}")

        for post in user.posts:
            print(
                f"  - {post.title} "
                f"({post.source})"
            )

        print()