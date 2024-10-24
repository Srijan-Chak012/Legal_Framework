import re
import string
import pandas as pd
import tqdm
# Read the CSV file into a pandas DataFrame
df = pd.read_csv('output.csv')
# get column acts/rules/orders from csv file
ip = df['Acts/Rules/Orders']

# Initialize an empty dictionary to store counts
act_counts = {}

# Loop through each row in the DataFrame
count = 0
for index, row in df.iterrows():

    input_string = row['Acts/Rules/Orders']
    if pd.isna(input_string):
        continue

    #  segraegate the acts based on comma abnd semicolon.
    acts = re.split(r'[;,]\s*', input_string)

    # if string starts with year then join with previous string
    for i in range(len(acts)):
        if acts[i].startswith('19') or acts[i].startswith('20'):
            acts[i-1] = acts[i-1] + ", " + acts[i]
            acts[i] = ''
        # remove \n and trailing spaces
        acts[i] = acts[i].replace('\n', '').strip()

    # remove empty strings
    acts = list(filter(None, acts))

    # Iterate through the entries and update the dictionary counts
    for entry in acts:
        # Trim any leading or trailing whitespaces to ensure key matching
        entry = entry.strip()
        act_counts[entry] = act_counts.get(entry, 0) + 1

# Print the dictionary with counts in the specified format
for act, count in act_counts.items():
    print(f'{act}: {count}')

# plot the graph
import matplotlib.pyplot as plt
plt.bar(range(len(act_counts)), list(act_counts.values()), align='center')
plt.xticks(range(len(act_counts)), list(act_counts.keys()), rotation=90)
plt.show()

# show 10 most frequent acts
import operator
sorted_act_counts = sorted(act_counts.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_act_counts[:10])

# show 10 least frequent acts
print(sorted_act_counts[-10:])

# make connection graph
import networkx as nx
G = nx.Graph()
for act, count in act_counts.items():
    G.add_node(act, count=count)
    for act2, count2 in act_counts.items():
        if act != act2:
            if act in act2:
                G.add_edge(act, act2)

nx.draw(G, with_labels=True)
plt.show()