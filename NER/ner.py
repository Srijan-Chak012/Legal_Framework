import os
import stanza
from tqdm import tqdm  # Import tqdm

# initialize the stanza pipeline with the English language model and the tokenize and ner processors
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

# read the text file
with open('constitution_of_india_article_14.txt') as f:
    text = f.read()

# create a stanza document object
doc = nlp(text)

print("Done till here")

# Create an output file
output_file = open('14_ner.txt', 'w')

# Create a tqdm progress bar
for sentence in tqdm(doc.sentences, desc='Processing sentences'):
    for entity in sentence.ents:
        output_file.write(f'{entity.text}\t{entity.type}\n')
    f.write('\n')

# close the output file
output_file.close()
