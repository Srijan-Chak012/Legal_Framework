import csv
import re

def read_selected_columns(file_path, selected_columns):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = []

        counter = 0

        for row in reader:
            counter += 1
            if counter == 6:
                break
            cases_referred = row["Cases Referred"]
            cases_list = cases_referred.split(";")
            case_list = [re.search(r"MANU/SC/\d+/\d+", case).group(0) if re.search(r"MANU/SC/\d+/\d+", case) else "" for case in cases_list]
            case_list = [case for case in case_list if case != ""]
            selected_data = {column: case_list if column == "Cases Referred" else row[column] for column in selected_columns}
            data.append(selected_data)

    return data

file_path = 'output.csv'
selected_columns = ["Manu_ID", "Cases Referred"]
data = read_selected_columns(file_path, selected_columns)



# Print sample output
for row in data:
    print("Manu_ID:", row["Manu_ID"])
    print("Cases Referred:", row["Cases Referred"])
    print("--------------------")
