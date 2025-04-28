# Catherine Team
# Core plugin
# original author: Vladislav Janvarev (Irene Voice Assistant)

from vacore import VACore

def start(core:VACore):
    manifest = {
        "name": "Core plugin",
        "version": "4.2",
        "description": "Plugin with Catherine's basic settings.\nTake a look at other plugins to see what commands you can use.",

        "options_label": {
            "mpcIsUse": "MPC Player Usage",
            "mpcHcPath": "MPC Player path",
            "mpcIsUseHttpRemote": "MPC Player usage via HTTP",

            "isOnline": "Online mode, require for online plugins like *gpt",
            # "ttsIndex": 0,
            "useTTSCache": "Cache text-to-speech (requires more disk space, may crash when switching voices)",
            "ttsEngineId": "ID of the main voice engine. If something doesn't work - try changing to pyttsx, elevenlabs, vosk, gpt (if you use it) or silero_v3 (the latter requires a full installation from install - i.e. from torch)",
            "ttsEngineId2": "ID of additional voice engine. Always voices the result on the machine where Kate is running (without web interface)",
            "playWavEngineId": "ID of the audio playback engine. If there are problems, try changing it to audioplayer or sounddevice",
            "linguaFrancaLang": "Language for lingua-franca",
            "voiceAssNames": "Names of the assistant. Use '|' as a delimiter.",
            "logPolicy": "all|cmd|none . All - log everything to console, cmd - only commands, none - never",  # all | cmd | none
            "replyNoCommandFound": "Answer when not understood",
            "replyNoCommandFoundInContext": "Response used for misunderstood in context",
            "replyOnlineRequired": "Response when calling offline a plugin function that requires online",

            "contextDefaultDuration": "Time in seconds while Catherine is in context (context is used in continuous chat, games, etc.; the word Kate|Catherine should not be used in context)",
            "contextRemoteWaitForCall": "(PRO) When using WEB-API - should I wait for a command from the client that the sound has already been played?",

            "tempDir": "Directory address for temporary files",
            "fuzzyThreshold": "(PRO) Confidence threshold when using fuzzy command recognition",

            "voiceAssNameRunCmd": "Comparisons dictionary. When finding the assistant's name, adds a prefix (comparison) to the recognized phrase",
        },

        "default_options": {
            "mpcIsUse": True,
            "mpcHcPath": "C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64_nvo.exe",
            "mpcIsUseHttpRemote": False,

            "isOnline": True,
            #"ttsIndex": 0,
            "useTTSCache": False,
            "ttsEngineId": "pyttsx",
            "ttsEngineId2": "", # engine for direct voice acting on the server. If empty - ttsEngineId is used
            "playWavEngineId": "audioplayer",
            "linguaFrancaLang": "en",
            "voiceAssNames": "kate|catherine|katherine|caitlin",
            "logPolicy": "cmd", # all | cmd | none

            "replyNoCommandFound": "Sorry, I didn't understand",
            "replyNoCommandFoundInContext": "Didn't understand...",
            "replyOnlineRequired": "This command requires online",

            "contextDefaultDuration": 10,
            "contextRemoteWaitForCall": False,

            "tempDir": "temp",
            "fuzzyThreshold": 0.5,

            "voiceAssNameRunCmd": {
                "albina": "chatgpt"
            }
        },

    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    #print(manifest["options"])
    options = manifest["options"]
    #core.setup_assistant_voice(options["ttsIndex"])

    core.mpcHcPath = options["mpcHcPath"]
    core.mpcIsUse = options["mpcIsUse"]
    core.mpcIsUseHttpRemote = options["mpcIsUseHttpRemote"]
    core.isOnline = options["isOnline"]

    core.voiceAssNames = options["voiceAssNames"].split("|")
    core.voiceAssNameRunCmd = options["voiceAssNameRunCmd"]
    print(core.voiceAssNameRunCmd)
    core.ttsEngineId = options["ttsEngineId"]
    core.ttsEngineId2 = options["ttsEngineId2"]
    core.playWavEngineId = options["playWavEngineId"]
    core.logPolicy = options["logPolicy"]

    core.contextDefaultDuration = options["contextDefaultDuration"]
    core.contextRemoteWaitForCall = options["contextRemoteWaitForCall"]

    core.tmpdir = options["tempDir"]
    import os
    if not os.path.exists(core.tmpdir):
        os.mkdir(core.tmpdir)

    core.useTTSCache = options["useTTSCache"]
    core.tts_cache_dir = "tts_cache"
    if not os.path.exists(core.tts_cache_dir):
        os.mkdir(core.tts_cache_dir)
    if not os.path.exists(core.tts_cache_dir+"/"+core.ttsEngineId):
        os.mkdir(core.tts_cache_dir+"/"+core.ttsEngineId)


    import lingua_franca
    lingua_franca.load_language(options["linguaFrancaLang"])


    return manifest
