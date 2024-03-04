from peewee import (
    SQL,
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    TextField,
)

db = SqliteDatabase("chatter.db")


class BaseModel(Model):
    class Meta:
        database = db


class ChatParticipants(BaseModel):
    user_id = CharField(primary_key=True)
    username = CharField(unique=True)
    display_name = CharField()
    participant_type = CharField()  # Consider using Enum in a real system
    email = CharField(null=True)
    password_hash = CharField(null=True)
    status = CharField()  # Active, Inactive, Suspended
    profile_icon = CharField(null=True)
    avatar = CharField(null=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])


class Thread(BaseModel):
    thread_id = AutoField()
    title = CharField(unique=True)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])


class Message(BaseModel):
    thread = ForeignKeyField(Thread, backref="messages")
    author = ForeignKeyField(ChatParticipants, backref="messages")
    role = CharField()  # user, agent, system
    content = TextField()
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])


class Subscriber(BaseModel):
    participant = ForeignKeyField(ChatParticipants, backref="subscriptions")
    thread = ForeignKeyField(Thread, backref="subscribers")
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])


class Notification(BaseModel):
    participant = ForeignKeyField(ChatParticipants, backref="notifications")
    thread = ForeignKeyField(Thread)
    message = ForeignKeyField(Message)
    timestamp = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])


def initialize_db():
    db.connect()
    db.create_tables(
        [ChatParticipants, Thread, Message, Subscriber, Notification], safe=True
    )


initialize_db()
