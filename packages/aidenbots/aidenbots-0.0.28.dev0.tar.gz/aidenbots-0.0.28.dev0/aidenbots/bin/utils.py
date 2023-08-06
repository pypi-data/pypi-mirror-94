import pkg_resources
import json
import subprocess


def play_alert_sound(sound):
    AUDIO_FILE_PATH = pkg_resources.resource_filename('aidenbots', 'sounds/' + sound)
    subprocess.run(['mpg123', AUDIO_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def import_custom_labware(custom_labware_file_name):
    labware_file = pkg_resources.resource_filename('aidenbots', 'labware/' + custom_labware_file_name +'.json')
    with open(labware_file) as labware_def:
        data = json.load(labware_def)
    return data

# def get_column_lists(number_of_columns=6):
#     for column in range(1, (number_of_columns + 1)):
#         left_column_names.append(str("A") + str(column))
#         right_column_names.append(str("A") + str(column + 6))
#         if (column % 2) == 0:
#             poz_neg_sequence.append(-1)
#         else:
#             poz_neg_sequence.append(1)


