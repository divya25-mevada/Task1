import pandas as pd

# Load the dataset
df = pd.read_csv("C:/Users/User/OneDrive/Desktop/netflix_titles.csv")


print("Missing values before cleaning:")
print(df.isnull().sum())

print("\nDuplicate rows before cleaning:", df.duplicated().sum())
df['director'] = df['director'].str.strip()
df['country'] = df['country'].str.strip()
df['cast'] = df['cast'].str.strip()
df['cast'] = df['cast'].str.replace(' ', ' ')
print("\nCurrent data types:")
print(df.dtypes)
df['show_id'] = df['show_id'].astype(str)
print("\nDuplicate rows after cleaning:", df.duplicated().sum())
df.to_csv('netflix_titles.csv', index=False)
