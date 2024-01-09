# from sqlalchemy import (
#     MetaData, Column, Table,
#     Boolean, Integer, String,
#     DateTime, ForeignKeyConstraint
# )

# metadata = MetaData()

# genre = Table(
#     "genre",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("title", String)
# )

# text = Table(
#     "text",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("title", String),
#     Column("content", String),
#     Column("date_created", DateTime),
#     Column("is_public", Boolean),
# )

# role = Table(
#     "role",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("title", String)
# )

# text_genre = Table(
#     "text_genre",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("text_id", Integer),
#     Column("genre_id", Integer),
#     ForeignKeyConstraint(["text_id"], ["text.id"]),
#     ForeignKeyConstraint(["genre_id"], ["genre.id"])
# )

# text_author = Table(
#     "text_author",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("text_id", Integer),
#     Column("user_id", Integer),
#     Column("role_id", Integer),
#     ForeignKeyConstraint(["text_id"], ["text.id"]),
#     ForeignKeyConstraint(["user_id"], ["user.id"]),
#     ForeignKeyConstraint(["role_id"], ["role.id"]),
# )