import csv
import pandas as pd
import re
import string
import json
import os

path = './output/'
writer = csv.writer(open('output.csv', 'wb'))

for file in os.listdir(path):
    df = dict()
    df['Appellant'] = []
    df['Respondent'] = []
    df['Counsel for Appellant'] = []
    df['Counsel for Respondent'] = []
    df['Judgement'] = ""
    file_name = os.fsdecode(file)
    with open(path + file) as input_file:
    # df = pd.read_csv('A . N . Sehgal and Ors . vs . Raje Ram Sheoram and Ors . ( 05 . 04 . 1991 - SC ).txt', header=None)
        case_note_index = -1
        counsel_index = -1
        count = 0
        case_category = -1
        for line in input_file:

            if line.startswith('JUDGMENT') or line.startswith('ORDER'):
                case_note_index = count

            if case_note_index != -1:
               df['Judgement'] += line.rstrip('\n')
               case_note_index = count

            if line.startswith('Case Note'):
                next_line = next(input_file)
                while next_line == '\n':
                    next_line = next(input_file)
                df['Case Note'] = next_line.rstrip('\n')

            elif line.startswith('Counsel'):
                counsel_index = count
            elif line.startswith('Case Category'):
                case_category = count
            elif line.startswith('Discussed'):
                # go next line till you find a line not empty
                next_line = next(input_file)
                while next_line == '\n':
                    next_line = next(input_file)
                df['discussed'] = next_line.rstrip('\n').strip(' ')
            elif line.startswith('Relied On'):
                next_line = next(input_file)
                while next_line == '\n':
                    next_line = next(input_file)
                df['relied on'] = next_line.rstrip('\n').strip(' ')

            # print(case_note_index)
            parts = line.split(':')
            # print(parts)
            if count == 0:
                match = parts[0].rstrip('\n')
                # print(match)
                df['Manu_ID'] = match
            elif count == 1:
                df['Court'] = parts[0].rstrip('\n')
                # print(df['Court'])
            elif count == 2:
                df['Case_No'] = parts[0].rstrip('\n')
                # print(df['Case_No'])
            elif count == 3:
                df['Date'] = parts[1].rstrip('\n')
                # print(df['Date'])
            if case_category != -1:
                df['Case Category'] = next(input_file).rstrip('\n').strip(' ')
                case_category = -1

        
            if parts[0].rstrip('\n') == 'Subject':
                df['Subject'] = parts[1].rstrip('\n')
            elif parts[0].rstrip('\n') == 'Disposition':
                next_line = next(input_file)
                while next_line == '\n':
                    next_line = next(input_file)
                df['Disposition'] = next_line.rstrip('\n').strip(' ')
            elif parts[0].rstrip('\n') == 'Hon\'ble Judges/Coram':
                next_line = next(input_file)
                while next_line == '\n':
                    next_line = next(input_file)
                df['Hon\'ble Judges/Coram'] = next_line.rstrip('\n').strip(' ')
            
            

            else:
                sentence_label = parts[0].rstrip('\n')
                
                if re.search('appellant', sentence_label, re.IGNORECASE) and re.search(':', line) and case_note_index == -1:
                    # join all parts of the sentence in parts[1] = parts[1] to parts[len(parts)-1]
                    join_sentence = ''
                    for i in range(1, len(parts)):
                        join_sentence += parts[i]
                        join_sentence += ":"
                    
                    parts[1] = join_sentence

                    if len(parts) > 1 and parts[1] is not None and counsel_index != -1:
                        df['Counsel for Appellant']+=parts[1].split(',')
                    elif counsel_index != -1:
                        next_line = next(input_file)
                        df['Counsel for Appellant']+=next_line.split(',')
                    elif len(parts) > 1 and parts[1] is not None:
                        df['Appellant']+=parts[1].split(',')
                    else:
                        # go to next line
                        next_line = next(input_file)
                        df['Appellant']+=next_line.split(',')

                elif re.search('respondent', sentence_label, re.IGNORECASE) and re.search(':', line) and case_note_index == -1:

                    join_sentence = ''
                    for i in range(1, len(parts)):
                        join_sentence += parts[i] 
                        join_sentence += ":"
                    
                    parts[1] = join_sentence
                    
                    if len(parts) > 1 and parts[1] is not None and counsel_index != -1:
                        df['Counsel for Respondent']+=parts[1].split(',')
                    elif counsel_index != -1:
                        next_line = next(input_file)
                        df['Counsel for Respondent']+=next_line.split(',')
                    elif len(parts) > 1 and parts[1] is not None:
                        df['Respondent']+=parts[1].split(',')
                    else:
                        next_line = next(input_file)
                        df['Respondent']+=next_line.split(',')
                
                elif re.search('Acts/Rules/Orders', sentence_label, re.IGNORECASE) and case_note_index == -1:
                    df['Acts/Rules/Orders'] = next(input_file).rstrip('\n').strip(' ')
                
                elif re.search('Cases Referred', sentence_label, re.IGNORECASE) and case_note_index == -1:
                    df['Cases Referred'] = next(input_file).rstrip('\n').strip(' ')
                
                elif re.search('Prior History:', sentence_label, re.IGNORECASE) and case_note_index == -1:
                    df['Prior History'] = next(input_file).rstrip('\n').strip(' ')
                
                elif re.search('Disposition:', sentence_label, re.IGNORECASE) and case_note_index == -1:
                    df['Disposition'] = next(input_file).rstrip('\n').strip(' ')
                
            


            count += 1
        
    # print(df)
        for key, value in df.items():
            if type(value) is list:
               print(key, value)
               for i, v in enumerate(value):
                   df[key][i] = v.strip().replace('\n', '')

            if type(value) is str:
                df[key] = value.strip().replace('\n', '')
            

        json_file = './output.json'

        # Load existing JSON data from the file (if any)
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            json_data = []

        # Append the new data to the JSON list
        json_data.append(df)

        # Write the updated JSON data back to the file
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=4)