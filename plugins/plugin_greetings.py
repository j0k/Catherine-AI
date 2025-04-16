# original author: Vladislav Janvarev (inspired by EnjiRouz)

import random
from vacore import VACore

# start function
def start(core:VACore):
    manifest = {
        "name": "Greeting",
        "version": "1.0",
        "require_online": False,
        "description": "Demo plugin\n"
                       "Voice command: hello|good morning",
        "commands": {
            "hello|good morning": play_greetings,
        }
    }
    return manifest

def play_greetings(core:VACore, phrase: str):
    greetings = [
        "Glad to see you!",
        "I am so glad to see my dear!",
    ]
    greet_str = greetings[random.randint(0, len(greetings) - 1)]
    print(f"- Now I say phrase {greet_str}...\nIf you don't hear it, then you have problems with TTS or sound output and you need to configure them through the settings manager.")
    core.play_voice_assistant_speech(greet_str)
    print(f"- I said {greet_str}")
