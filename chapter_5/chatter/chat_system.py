from datetime import datetime

from peewee import *

from chatter.action_manager import ActionManager
from chatter.agent_manager import AgentManager
from chatter.chat_models import (
    ChatParticipants,
    Message,
    Notification,
    Subscriber,
    Thread,
    db,
)


class ChatSystem:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.load_agents()

        self.action_manager = ActionManager()
        self.actions = self.load_actions()

    def load_actions(self):
        actions = self.action_manager.get_actions()
        print(f"Loaded {len(actions)} actions.")
        return actions

    def load_agents(self):
        agents = self.agent_manager.get_agent_names()
        avatars = ["🤖", "🧠", "🧮", "⚙️", "🔮"]  # more than 5 agents add more icons
        avatars.reverse()  # better emojis at the start
        for agent in agents:
            participant = (
                ChatParticipants.select()
                .where(ChatParticipants.username == agent)
                .first()
            )
            if not participant:
                self.add_participant(
                    agent,
                    participant_type="agent",
                    display_name=agent,
                    avatar=avatars.pop(),
                )

    def get_agent(self, agent_name):
        agent = self.agent_manager.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        agent.actions = self.action_manager.get_actions()
        return agent

    def get_agent_names(self):
        return self.agent_manager.get_agent_names()

    def add_participant(
        self,
        username,
        password_hash="",
        display_name=None,
        participant_type="user",
        email="",
        status="inactive",
        profile_icon="",
        avatar="",
    ):
        with db.atomic():
            if (
                ChatParticipants.select()
                .where(ChatParticipants.user_id == username)
                .exists()
            ):
                raise ValueError("Participant ID already exists")
            ChatParticipants.create(
                user_id=username,
                username=username,
                display_name=display_name,
                participant_type=participant_type,
                email=email,
                password_hash=password_hash,
                status=status,
                profile_icon=profile_icon,
                avatar=avatar,
            )
            print(f"Participant '{username}' added.")
            return True

    def get_participant(self, username):
        return ChatParticipants.get(ChatParticipants.username == username)

    def create_thread(self, title, participant_id):
        with db.atomic():
            thread = Thread.create(title=title)
            Subscriber.create(participant=participant_id, thread=thread)
            return thread

    def get_all_threads(self):
        return Thread.select()

    def get_thread(self, thread_id):
        return Thread.get(Thread.thread_id == thread_id)

    def subscribe_to_thread(self, thread_id, participant_id):
        with db.atomic():
            if (
                not Subscriber.select()
                .where(
                    Subscriber.participant == participant_id,
                    Subscriber.thread == thread_id,
                )
                .exists()
            ):
                Subscriber.create(participant=participant_id, thread=thread_id)
            else:
                print(
                    f"Participant {participant_id} is already subscribed to thread {thread_id}."
                )

    def leave_thread(self, thread_id, participant_id):
        with db.atomic():
            query = Subscriber.delete().where(
                Subscriber.participant == participant_id, Subscriber.thread == thread_id
            )
            query.execute()

    def post_message(self, thread_id, participant_id, role, content):
        with db.atomic():
            message = Message.create(
                thread=thread_id,
                author=participant_id,
                content=content,
                role=role,
                timestamp=datetime.now(),
            )
            subscribers = Subscriber.select().where(Subscriber.thread == thread_id)
            for subscriber in subscribers:
                if subscriber.participant.user_id != participant_id:
                    Notification.create(
                        participant=subscriber.participant,
                        thread=thread_id,
                        message=message,
                    )

    def read_messages(self, thread_id):
        return (
            Message.select()
            .where(Message.thread == thread_id)
            .order_by(Message.timestamp.asc())
        )

    def get_user_notifications(self, participant_id):
        return Notification.select().where(Notification.participant == participant_id)

    def get_threads_for_user(self, participant_id):
        query = (
            Thread.select()
            .join(Subscriber)
            .where(Subscriber.participant == participant_id)
            .order_by(Thread.timestamp.desc())
        )
        return list(query.execute())

    def login(self, username, password_hash):
        participant = (
            ChatParticipants.select()
            .where(ChatParticipants.username == username)
            .first()
        )
        if participant:
            # In a real application, compare hashed passwords instead
            if participant.password_hash == password_hash:
                participant.status = "Active"
                participant.save()
                print(f"{username} logged in successfully.")
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("Username not found.")
            return False

    def logout(self, username):
        participant = (
            ChatParticipants.select()
            .where(ChatParticipants.username == username)
            .first()
        )
        if participant:
            participant.status = "Inactive"
            participant.save()
            print(f"{username} logged out successfully.")
        else:
            print("Username not found.")
