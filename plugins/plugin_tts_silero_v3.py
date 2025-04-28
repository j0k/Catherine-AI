# TTS plugin for silero engine

# author of original Irina version: Vladislav Janvarev

# require torch 1.10+

# model list https://models.silero.ai/models/tts/


modelurl = 'https://models.silero.ai/models/tts/en/v3_en.pt'

import os
from vacore import VACore

modname = os.path.basename(__file__)[:-3] # calculating modname


def start(core:VACore):
    manifest = {
        "name": "TTS silero V3",
        "version": "2.0",
        "require_online": False,

        "default_options": {
            "speaker": "en_88",
            "threads": 4,
            "sample_rate": 24000,
            "put_accent": True,
            "put_yo": True
        },

        "tts": {
            "silero_v3": (init,None,towavfile) # первая функция инициализации, вторая - говорить
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def init(core:VACore):
    options = core.plugin_options(modname)

    import os
    import torch

    device = torch.device('cpu')
    torch.set_num_threads(options["threads"])
    local_file = 'silero_model.pt'

    if not os.path.isfile(local_file):
        print("Downloading Silero model...")
        torch.hub.download_url_to_file(modelurl,
                                       local_file)

    core.model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    core.model.to(device)


def towavfile(core:VACore, text_to_speech:str, wavfile:str):
    text_to_speech = text_to_speech.replace("…","...")
    text_to_speech = core.all_num_to_text(text_to_speech)
    #print(text_to_speech)


    options = core.plugin_options(modname)
    speaker = options["speaker"]


    # wav rendering
    path = core.model.save_wav(text=text_to_speech,
                               speaker=speaker,
                               put_accent=options["put_accent"],
                               put_yo=options["put_yo"],
                               sample_rate=options["sample_rate"])

    # move wav file to new place
    if os.path.exists(wavfile):
        os.unlink(wavfile)
    os.rename(path,wavfile)
