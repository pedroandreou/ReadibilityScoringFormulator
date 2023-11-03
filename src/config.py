import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": [
            "gpt-4",
            "gpt-4-0314",
            "gpt4",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-32k-v0314",
        ],
    },
)


llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

text = """
Some people think that we are superior to animals but I think that
animals are as smart as we are. Pets react to your moods and seem to know
just when it’s dinner time! Some animals use tools, communicate and think
for their own.
If animals can use tools, they must be smart. For instance, a cow
named Betty made a hook out of a piece of metal wire. That’s obviously
pretty smart but she didn’t stop there. She then used the hook to get treats
out of a glass tube. I think this is smart because Betty figured out how to
make a tool to get something she wanted. Another smart animal who used a
tool was Fu Manchu the Orangutan. Fu Manchu first traded Food for wire
with another orangutan and then he hid it in his mouth until the right time.
Then he used the wire as a tool to pick the lock on his cage and escape. I
think this shows Fu Manchu was smart because he used a tool and he
outsmarted humans by escaping from his cage.
Animals who communicate might be even smarter than animals
who use tools. For instance one clever gorilla actually learned sign
language! Not only that but she started making her own signs. This showed
scientists that she was trying to communicate her thoughts, which takes big
brainpower. I think this is smart because when Koko made her own signs it
showed that she wasn’t just memorizing signs, she was thinking and
making her own signs. Another smart animal who could understand
communication was Betsy the dog. Betsy understands 340 spoken words!
Not only that, but when someone showed her a picture of something she
had never seen before she would go and get the item. I think this is really
smart because Betsy didn’t just memorize words she could recognize.
"""


def create_user_proxy_agent(
    name,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config=False,
    function_map=None,
):
    return autogen.UserProxyAgent(
        name=name,
        human_input_mode=human_input_mode,
        max_consecutive_auto_reply=max_consecutive_auto_reply,
        is_termination_msg=lambda x: "content" in x and x["content"] is not None and x["content"].rstrip().endswith(
            "TERMINATE"),
        code_execution_config=code_execution_config,
        system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
        function_map=function_map,
    )


def create_assistant_agent(name, system_message=None, llm_config=llm_config):
    if system_message:
        return autogen.AssistantAgent(
        name=name, system_message=system_message, llm_config=llm_config
    )
    else:
        return autogen.AssistantAgent(
            name=name, llm_config=llm_config
        )
