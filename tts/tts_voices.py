import os

module_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(module_dir, 'voice_table.txt')
with open(file_path, 'r') as f:
    text = f.read()
    rows2 = text.split('\n')

file_path = os.path.join(module_dir, 'voice_table_3.txt')
with open(file_path, 'r') as f:
    text = f.read()
    rows3 = text.split('\n')

file_path = os.path.join(module_dir, 'voice_table_7.txt')
with open(file_path, 'r') as f:
    text = f.read()
    rows7 = text.split('\n')

    voice_dict = {}

    for row in rows2:
        columns = row.split()

        if len(columns) >= 5:
            language = columns[0]
            voice_name = columns[2]
            lang_id = int(columns[1])
            voice_id = int(columns[3])
            gender = columns[4]
            description = ' '.join(columns[5:])

            voice_data = [2, lang_id, voice_id, gender, description, language]
            voice_dict[voice_name] = voice_data

    for row in rows3:
        columns = row.split()

        if len(columns) >= 5:
            language = columns[0]
            voice_name = columns[2]
            lang_id = int(columns[1])
            voice_id = int(columns[3])
            gender = columns[4]
            description = ' '.join(columns[5:])

            voice_data = [3, lang_id, voice_id, gender, description, language]
            voice_dict[voice_name] = voice_data

    for row in rows7:
        columns = row.split()

        if len(columns) >= 5:
            language = columns[0]
            voice_name = columns[2]
            lang_id = int(columns[1])
            voice_id = int(columns[3])
            gender = columns[4]
            description = ' '.join(columns[5:])

            voice_data = [7, lang_id, voice_id, gender, description, language]
            voice_dict[voice_name] = voice_data

