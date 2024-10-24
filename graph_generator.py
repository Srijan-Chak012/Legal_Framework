import csv
import re
import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# Increase the field size limit
csv.field_size_limit(sys.maxsize)

def read_selected_columns(file_path, selected_columns):
    global counter
    counter = 0
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = []

        for row in reader:
            counter += 1
            # if counter == 6:
            #     break
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

# for row in data:
#     print("Manu_ID:", row["Manu_ID"])
#     print("Cases Referred:", row["Cases Referred"])
#     print("--------------------")

dictionary = {row["Manu_ID"]: row["Cases Referred"] for row in data}

with open("dictionary_output.json", "w") as f:
    json.dump(dictionary, f)

print(counter)

key_counts = Counter(dictionary.keys())

# Count the occurrences of each node in the values of the original dictionary
value_counts = Counter(node for connections in dictionary.values() for node in connections)

# Combine the key and value counts
combined_counts = {node: key_counts[node] + value_counts.get(node, 0) for node in set(key_counts) | set(value_counts)}

# print(combined_counts)

with open("dictionary_output2.json", "w") as f:
    json.dump(combined_counts, f)

# Create an empty directed graph
graph = nx.DiGraph()

# Add nodes to the graph with serial numbers as labels
serial_number = 1
node_labels = {}  # Store the mapping of serial number to node label
for node, count in combined_counts.items():
    graph.add_node(serial_number)
    node_labels[serial_number] = str(serial_number)
    serial_number += 1

with open("dictionary_output3.json", "w") as f:
    json.dump(node_labels, f)

# Add edges based on the original dictionary
for node, connections in dictionary.items():
    source = list(combined_counts.values())[list(combined_counts.keys()).index(node)]
    for connection in connections:
        target = list(combined_counts.values())[list(combined_counts.keys()).index(connection)]
        graph.add_edge(source, target)

# Draw the graph with serial numbers as node labels
nx.draw(graph, labels=node_labels, with_labels=True, node_size=1000, node_color='lightblue', font_weight='bold')

# Save and Display the graph
plt.savefig("graph.png")
plt.show()