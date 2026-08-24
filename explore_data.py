import pandas as pd

# Load the dataset
df = pd.read_csv("train 2.csv", on_bad_lines="skip", engine="python")

# Basic look at the data
print("Shape (rows, columns):", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

print("\nLabel counts:")
print(df["label"].value_counts())
# Look at a sample of actual text to understand the mix of languages
print("\nSample texts:")
for text in df["text"].head(10):
    print("-", text[:150])
    import re

# Devanagari Unicode range (covers Hindi script)
devanagari_pattern = re.compile(r'[\u0900-\u097F]')

def is_hindi_english_mix(text):
    text = str(text)
    has_devanagari = bool(devanagari_pattern.search(text))
    has_latin = bool(re.search(r'[a-zA-Z]', text))
    return has_devanagari and has_latin

# Filter the dataset to Hindi-English code-switched rows only
df["is_codeswitch"] = df["text"].apply(is_hindi_english_mix)
codeswitch_df = df[df["is_codeswitch"]]

print("\nTotal Hindi-English code-switched rows found:", len(codeswitch_df))
print("\nSample of filtered rows:")
for text in codeswitch_df["text"].head(5):
    print("-", text[:150])
    print("\nLength check on first 10 rows:")
for i, text in enumerate(df["text"].head(10)):
    print(f"Row {i}: {len(str(text))} characters")
print("\nFull text of row 0:")
print(df["text"].iloc[0])
print("\nSentiment breakdown of code-switched rows only:")
print(codeswitch_df["label"].value_counts())

print("\nSentiment breakdown of ALL rows (for comparison):")
print(df["label"].value_counts())
print("\nPercentage breakdown - code-switched:")
print((codeswitch_df["label"].value_counts(normalize=True) * 100).round(2))

print("\nPercentage breakdown - all data:")
print((df["label"].value_counts(normalize=True) * 100).round(2))
import matplotlib.pyplot as plt

labels = ["Negative", "Neutral", "Positive"]
codeswitch_pct = [34.18, 33.51, 32.31]  # from your output above
overall_pct = [33.33, 33.33, 33.33]

x = range(len(labels))
plt.bar([i - 0.2 for i in x], codeswitch_pct, width=0.4, label="Code-switched")
plt.bar([i + 0.2 for i in x], overall_pct, width=0.4, label="Overall dataset")
plt.xticks(list(x), labels)
plt.ylabel("Percentage (%)")
plt.title("Sentiment Distribution: Code-switched vs Overall Reviews")
plt.legend()
plt.savefig("sentiment_comparison.png")
plt.show()