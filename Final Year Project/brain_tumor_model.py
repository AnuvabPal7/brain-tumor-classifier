import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
data = pd.read_csv("brain_tumor_dataset.csv")
target_col = "Tumor"
X = data.drop(target_col, axis=1)
y = data[target_col]
y = LabelEncoder().fit_transform(y)
X = pd.get_dummies(X, drop_first=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
importances = model.feature_importances_
features = X.columns
plt.figure()
plt.barh(features, importances)
plt.xlabel("Importance")
plt.ylabel("Features")
plt.title("Feature Importance in Tumor Prediction")
plt.show()
sample = X_test.iloc[[0]]
prediction = model.predict(sample)
if prediction[0] == 1:
    print("\nResult: Brain Tumor Predicted ⚠️")
else:
    print("\nResult: No Brain Tumor Predicted ✅")