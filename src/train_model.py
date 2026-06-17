import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

# -------------------------------------------------
# 1. Load data
# -------------------------------------------------
data = pd.read_csv("data/new_brain_tumor_dataset.csv")
data = data.drop(columns=["Image"])
target_col = "Class"
X = data.drop(target_col, axis=1)
y = data[target_col]

# -------------------------------------------------
# 2. Train/test split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features (helps Logistic Regression / SVM; RF doesn't need it but doesn't hurt)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------------------------
# 3. Baseline model comparison
# -------------------------------------------------
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(probability=True, random_state=42),
}

print("=" * 50)
print("BASELINE MODEL COMPARISON (5-fold CV accuracy)")
print("=" * 50)

for name, model in models.items():
    if name == "Random Forest":
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    else:
        scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="accuracy")
    print(f"{name:20s}: mean={scores.mean():.4f}  std={scores.std():.4f}")

# -------------------------------------------------
# 4. Hyperparameter tuning for Random Forest
# -------------------------------------------------
print("\n" + "=" * 50)
print("HYPERPARAMETER TUNING (Random Forest)")
print("=" * 50)

param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    verbose=1,
)
grid_search.fit(X_train, y_train)

print("\nBest params:", grid_search.best_params_)
print(f"Best CV accuracy: {grid_search.best_score_:.4f}")

best_model = grid_search.best_estimator_

# -------------------------------------------------
# 5. Final evaluation on held-out test set
# -------------------------------------------------
y_pred = best_model.predict(X_test)

print("\n" + "=" * 50)
print("FINAL TEST SET EVALUATION")
print("=" * 50)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------------------------------
# 6. Confusion matrix
# -------------------------------------------------
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Tumor", "Tumor"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix - Random Forest (Tuned)")
plt.tight_layout()
plt.savefig("results/confusion_matrix.png", dpi=150)
plt.close()
print("\nSaved results/confusion_matrix.png")

# -------------------------------------------------
# 7. Feature importance
# -------------------------------------------------
importances = best_model.feature_importances_
features = X.columns

plt.figure(figsize=(8, 6))
sorted_idx = np.argsort(importances)
plt.barh(features[sorted_idx], importances[sorted_idx])
plt.xlabel("Importance")
plt.title("Feature Importance - Random Forest (Tuned)")
plt.tight_layout()
plt.savefig("results/feature_importance.png", dpi=150)
plt.close()
print("Saved results/feature_importance.png")

# -------------------------------------------------
# 8. SHAP explainability
# -------------------------------------------------
print("\n" + "=" * 50)
print("SHAP EXPLAINABILITY")
print("=" * 50)

explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test)

# For binary classification, shap_values is a list [class0, class1] in older SHAP versions,
# or a single array with shape (n_samples, n_features, n_classes) in newer versions.
if isinstance(shap_values, list):
    shap_values_for_plot = shap_values[1]  # class 1 = "Tumor"
elif shap_values.ndim == 3:
    shap_values_for_plot = shap_values[:, :, 1]
else:
    shap_values_for_plot = shap_values

plt.figure()
shap.summary_plot(shap_values_for_plot, X_test, show=False)
plt.tight_layout()
plt.savefig("results/shap_summary.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved results/shap_summary.png")

# -------------------------------------------------
# 9. Sample prediction
# -------------------------------------------------
sample = X_test.iloc[[0]]
prediction = best_model.predict(sample)
proba = best_model.predict_proba(sample)[0]

print("\n" + "=" * 50)
print("SAMPLE PREDICTION")
print("=" * 50)
if prediction[0] == 1:
    print(f"Result: Brain Tumor Predicted (confidence: {proba[1]:.2%})")
else:
    print(f"Result: No Brain Tumor Predicted (confidence: {proba[0]:.2%})")

# -------------------------------------------------
# 10. Save model for Streamlit app
# -------------------------------------------------
import joblib
joblib.dump(best_model, "models/brain_tumor_rf_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("\nSaved models/brain_tumor_rf_model.pkl and models/scaler.pkl")