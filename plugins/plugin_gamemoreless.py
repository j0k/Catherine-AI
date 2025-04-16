# Game more less
# original author: Vladislav Janvarev

from datetime import datetime

from vacore import VACore
import random

def start(core:VACore):
    manifest = {
        "name": "Game more less",
        "version": "1.0",
        "require_online": False,
        "description": "Demo game\n"
                       "Voice command: play more less",
        "commands": {
            "play more less|play more or less": play_game_start,
        }
    }
    return manifest

questNumber = -1
tries = 0

def play_game_start(core:VACore, phrase: str):
    core.play_voice_assistant_speech("Tell me the rules or start")
    core.context_set(play_1)

def play_1(core:VACore, phrase: str):
    if phrase == "rules":
        core.play_voice_assistant_speech("Rules of the game. I guess of a number from one to thirty."
                                        "You say a number and I say whether the number you think of is greater or less than the one you said."
                                        "Your task is to guess the number in ten tries. Say start to start the game.")
        core.context_set(play_1)
        return
    if phrase == "start" or phrase == "repeat":
        global questNumber, tries
        questNumber = random.randint(1,30)
        print(questNumber)
        tries = 0
        core.play_voice_assistant_speech("A number from one to thirty is guessed. Let's begin!")
        core.context_set(play_2)
        return

    if phrase == "cancel" or phrase == "goodbye":
        core.say("Got it, we won't play.")
        return

    core.play_voice_assistant_speech("Don't understand...")
    core.context_set(play_1)

def play_2(core:VACore, phrase: str):
    from lingua_franca.format import pronounce_number
    for i in range(1,31):
        #print(pronounce_number(i), phrase)
        if phrase == pronounce_number(i):
            global tries
            tries += 1
            if i == questNumber:
                core.say("Yes, you guessed it. Congratulations on your win! Tell me repeat if you want to play again.")
                core.context_set(play_1)
                return
            else:
                txtsay = ""
                if i < questNumber:
                    txtsay += "More."
                else:
                    txtsay += "Less."

                if tries >= 10:
                    txtsay += "Ten attempts have passed, unfortunately, you lost. And I guessed a number "+pronounce_number(questNumber)
                    txtsay += ". Tell me to repeat if you want to play again."
                    core.say(txtsay)
                    core.context_set(play_1)
                    return
                else:
                    core.say(txtsay)
                    core.context_set(play_2)
                    return

    core.play_voice_assistant_speech("I didn't understand the number, tell me again!")
    core.context_set(play_2)
