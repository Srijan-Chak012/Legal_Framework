import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('manupatra_anno.csv')

# Ensure 'Case Topics' is treated as strings and handle non-string cases
df['Case Topics'] = df['Case Topics'].astype(str).fillna('')

# Step 1: One-hot encode the 'Case Topics' column
# Split the topics only if the value is a valid string
topics_one_hot = df['Case Topics'].apply(
    lambda x: pd.Series(1, index=[topic.strip() for topic in x.split(',') if isinstance(topic, str)])
).fillna(0)
# Step 2: One-hot encode the 'Appellant Type' column (direct one-hot encoding)
# Step 2: Filter out topics with fewer than 5 occurrences
topic_counts = topics_one_hot.sum(axis=0)  # Count occurrences of each topic
filtered_topics = topic_counts[topic_counts >= 5].index  # Keep only topics with >= 5 occurrences
topics_one_hot = topics_one_hot[filtered_topics]  # Filter the one-hot encoded DataFrame

appellant_one_hot = pd.get_dummies(df['Appelant Category'])

# Step 3: Combine both one-hot encoded DataFrames
combined_df = pd.concat([topics_one_hot, appellant_one_hot], axis=1)

# Step 4: Perform correlation analysis
# You can use the Pearson correlation or Spearman correlation (Spearman is used for non-linear relationships)
correlation_matrix = combined_df.corr(method='pearson')  # Or 'spearman'

# Step 5: Filter the correlation results to show only the correlations between Case Topics and Appellant Type
# Extract relevant rows (topics) and columns (appellant types)
case_topics = topics_one_hot.columns
appellant_types = appellant_one_hot.columns
correlation_results = correlation_matrix.loc[case_topics, appellant_types]

correlation_results.to_csv('correlation_matrix.csv', index=True)

# Print the correlation matrix
print("Correlation matrix between 'Case Topics' and 'Appellant Type':")
print(correlation_results)

# Step 6: Plot the heatmap
plt.figure(figsize=(14, 10))  # Adjust the figure size as needed
sns.heatmap(correlation_results, annot=True, cmap='coolwarm', center=0, linewidths=.5)
plt.title('Correlation between Case Topics and Appellant Type')
plt.xlabel('Appellant Type')
plt.ylabel('Case Topics')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout for better fit
plt.savefig('correlation_heatmap.png', dpi=300)  # Save the heatmap as an image
plt.show()