import pandas as pd
import os
from feature_extraction import extract_features

labels_df = pd.read_csv("data/Brain Tumor.csv")

rows = []

image_folder = r"dataset\Brain Tumor"

for _, row in labels_df.iterrows():
    image_name = row["Image"]
    label = row["Class"]

    image_path = os.path.join(image_folder, image_name + ".jpg")

    if not os.path.exists(image_path):
        continue

    try:
        features = extract_features(image_path)

        features["Class"] = label
        features["Image"] = image_name

        rows.append(features)

    except Exception as e:
        print(f"Error processing {image_name}: {e}")

new_df = pd.DataFrame(rows)

new_df.to_csv("data/new_brain_tumor_dataset.csv", index=False)
print("Rows:", len(new_df))
print("Saved new_brain_tumor_dataset.csv")