# gpt openai
# original author: Vladislav Janvarev

import os
import openai

from vacore import VACore

import json
import os
import openai

import socks
import socket
#proxy_url = "socks5://ip:port"

#if proxy_url and len(proxy_url)>0:
#    proxy_parts = proxy_url.split("://")[1].split(":")
#    socks.set_default_proxy(socks.SOCKS5, proxy_parts[0], int(proxy_parts[1]))
#    socket.socket = socks.socksocket

# ---------- from https://github.com/stancsz/chatgpt ----------
# gpt-3.5-turbo
# deepseek-chat
# gpt-4-1106-preview
class ChatApp:
    def __init__(self, model="gpt-3.5-turbo", load_file='', system=''):
        # Setting the API key to use the OpenAI API
        self.model = model
        self.messages = []
        if system != '':
            self.messages.append({"role": "system", "content" : system})
        if load_file != '':
            self.load(load_file)

    def chat(self, message):
        if message == "exit":
            self.save()
            os._exit(1)
        elif message == "save":
            self.save()
            return "(saved)"
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0.8,
            n=1,
            max_tokens=100,
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]

    def save(self):
        try:
            import time
            import re
            import json
            ts = time.time()
            json_object = json.dumps(self.messages, indent=4)
            filename_prefix=self.messages[0]['content'][0:30]
            filename_prefix = re.sub('[^0-9a-zA-Z]+', '-', f"{filename_prefix}_{ts}")
            with open(f"models/chat_model_{filename_prefix}.json", "w") as outfile:
                outfile.write(json_object)
        except:
            os._exit(1)

    def load(self, load_file):
        with open(load_file) as f:
            data = json.load(f)
            self.messages = data

modname = os.path.basename(__file__)[:-3] # calculating modname

# start here
def start(core:VACore):

    manifest = {
        "name": "ChatGPT speaker OpenAI v2",
        "version": "2.0",
        "require_online": True,
        "description": "Allows you to communicate with ChatGPT using specified apiKey.\n"
                       "Voice command: let's speak|let's talk",
        "url": "https://github.com/janvarev/irene_plugin_boltalka2_openai",

        "options_label": {
            "apiKey": "API-key for OpenAI or similar", #
            "apiBaseUrl": "URL for OpenAI (can provide yours URL with same to OpenAI interface)",  #
            "system": "An intro personal line which specifies the nature of the assistant."
        },

        "default_options": {
            "apiKey": "", #
            "apiBaseUrl": "",  #
            "system": "Your name is Catherine. You is a voice business assistant who helps entrepreneurs to solve their problems. Give short, plain and to the point answers."
        },

        "commands": {
            "let's speak|let's talk|let's chat|let talk": run_start,
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def run_start(core:VACore, phrase:str):
    options = core.plugin_options(modname)

    if options["apiKey"] == "" and options["apiBaseUrl"] == "":
        core.play_voice_assistant_speech("Need api key to access openai")
        return

    openai.api_key = options["apiKey"]
    if options["apiBaseUrl"] != "":
        openai.api_base = options["apiBaseUrl"]

    core.chatapp = ChatApp(system=options["system"]) # creating new chat
    if phrase == "":
        core.play_voice_assistant_speech("Yes, of course!")
        core.context_set(boltalka, 20)
    else:
        boltalka(core,phrase)

def boltalka(core:VACore, phrase:str):
    if phrase == "cancel" or phrase == "goodbye" or phrase == "exit":
        core.play_voice_assistant_speech("goodbye!")
        return

    try:
        response = core.chatapp.chat(phrase) #generate_response(phrase)
        print(response)
        #decoded_value = response.encode('utf-8')
        #print(decoded_value)
        core.say(response["content"])
        core.context_set(boltalka, 20)

    except:
        import traceback
        traceback.print_exc()
        core.play_voice_assistant_speech("Problems with OpenAI API")

        return
