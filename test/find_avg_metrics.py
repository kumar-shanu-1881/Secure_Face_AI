import pandas as pd 

df=pd.read_csv("../similarity_results.csv")
print(df.head())

print(df.info())

print(df.describe())

avg_cosine_similarity=df['Cosine Similarity'].sum()/1097
print(avg_cosine_similarity)

print(df['Predicted'].value_counts())