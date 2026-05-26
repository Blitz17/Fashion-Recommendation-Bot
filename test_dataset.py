import pandas as pd

df = pd.read_csv("dataset/styles.csv", on_bad_lines="skip")

print(df.head())

print("\nColumns:\n")
print(df.columns)

print("\nTotal Rows:", len(df))

columns_to_check = [
    "articleType",
    "usage",
    "gender",
    "baseColour"
]

for column in columns_to_check:

    print(f"\n{'=' * 50}")
    print(column.upper())
    print(f"{'=' * 50}\n")

    values = sorted(
        df[column]
        .dropna()
        .unique()
    )

    print(values)