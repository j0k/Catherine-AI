#
#
# MIT License
# Original author Janvarev Vladislav (Irene repo)
#
# library for translate all digits in text to pronounce

import re

from lingua_franca.format import pronounce_number

def load_language(lang:str):
    import lingua_franca
    lingua_franca.load_language(lang)

def convert_one_num_float(match_obj):
    if match_obj.group() is not None:
        text = str(match_obj.group())
        return pronounce_number(float(match_obj.group()))

def convert_diapazon(match_obj):
    if match_obj.group() is not None:
        text = str(match_obj.group())
        text = text.replace("-"," dash ")
        return all_num_to_text(text)


def all_num_to_text(text:str) -> str:
    text = re.sub(r'[\d]*[.][\d]+-[\d]*[.][\d]+', convert_diapazon, text)
    text = re.sub(r'-[\d]*[.][\d]+', convert_one_num_float, text)
    text = re.sub(r'[\d]*[.][\d]+', convert_one_num_float, text)
    text = re.sub(r'[\d]-[\d]+', convert_diapazon, text)
    text = re.sub(r'-[\d]+', convert_one_num_float, text)
    text = re.sub(r'[\d]+', convert_one_num_float, text)
    text = text.replace("%", " процентов")
    return text
