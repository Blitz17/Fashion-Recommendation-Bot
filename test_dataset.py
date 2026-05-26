import pandas as pd

df = pd.read_csv("dataset/styles.csv", on_bad_lines="skip")

print(df.head())

print("\nColumns:\n")
print(df.columns)

print("\nTotal Rows:", len(df))