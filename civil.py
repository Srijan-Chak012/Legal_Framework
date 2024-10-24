import pandas as pd
import re
import gensim
import gensim.corpora as corpora
import nbformat
import nltk

from gensim.models import LdaModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

nltk.download('stopwords')

from nltk.corpus import stopwords

# Let's load the provided file and inspect the content to understand how the topic modeling is being performed in the notebook.
file_path = './topics.ipynb'

# Load the notebook content
with open(file_path, 'r', encoding='utf-8') as f:
    notebook_content = nbformat.read(f, as_version=4)

# Check the cells in the notebook to understand the content and logic
notebook_content['cells']

print("Done Till Here")

# Load stop words
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

# Load the CSV file with case topics and judgement
df = pd.read_csv('./manupatra_anno.csv')

# Filter cases where 'case topics' contain 'civil' or 'constitutional'
df_filtered = df[df['Case Topics'].str.contains('Civil/Constitutional', case=False, na=False)]

# Combine all text from the 'Judgement' column
judgement_text = df_filtered['Judgement'].dropna().tolist()

# Preprocessing function
def preprocess(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    #Remove single characters
    text = re.sub(r'\b\w\b', '', text)
    # Remove numbers
    text = re.sub(r'\b\d+\b', '', text)
    text = text.lower()  # Convert to lowercase
    tokens = text.split()  # Tokenize the text
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    return tokens

# Preprocess all judgement texts
processed_texts = [preprocess(text) for text in judgement_text]

# Create a dictionary and corpus
dictionary = corpora.Dictionary(processed_texts)
corpus = [dictionary.doc2bow(text) for text in processed_texts]

# Train the LDA model with 10 topics
lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15, random_state=42)

# Prepare the visualization data
lda_display = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)

# Save the visualization as an HTML file
pyLDAvis.save_html(lda_display, 'lda_visualization.html')

print("LDA visualization saved as lda_visualization.html")