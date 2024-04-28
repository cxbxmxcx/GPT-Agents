from autogen import (
    AssistantAgent,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
    config_list_from_json,
)
from autogen.cache import Cache

# Load the configuration list from the config file.
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

# Create the agent that represents the user in the conversation.
user_proxy = UserProxyAgent(
    "user",
    code_execution_config={
        "work_dir": "working",
        "use_docker": False,
        "last_n_messages": 3,
    },
    human_input_mode="NEVER",
)

llm_config = {"config_list": config_list}

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""
    You are a profession Python engineer, known for your expertise in software development.
    You use your skills to create software applications, tools, and games that are both functional and efficient.
    Your preference is to write clean, well-structured code that is easy to read and maintain.    
    """,
)

critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""
    Critic. You are a game engineer and master in evaluating the quality of a given game code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER GAMING BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
    - bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
    - Game play: how well does the game play? Is it engaging, fun, and challenging? Are there any game play elements that could be improved?
    - Goal compliance (compliance): how well the code meets the specified gaming goals?    
    - aesthetics (aesthetics): Are the aesthetics of the game appropriate for the theme type and the data?

    YOU MUST PROVIDE A SCORE for each of the above dimensions.
    {bugs: 0, transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
    Do not suggest code.
    Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
    """,
)

groupchat = GroupChat(agents=[user_proxy, engineer, critic], messages=[], max_round=20)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

task = """Write a snake game using Pygame."""

with Cache.disk(cache_seed=43) as cache:
    res = user_proxy.initiate_chat(
        recipient=manager,
        message=task,
        cache=cache,
    )
