import streamlit as st
import pandas as pd
import joblib
import sys
from pathlib import Path

# -------------------------------------------------
# Project paths
# -------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT / "src"))

from feature_extraction import extract_features

# -------------------------------------------------
# Load trained model
# -------------------------------------------------
model = joblib.load(ROOT / "models" / "brain_tumor_rf_model.pkl")

FEATURE_ORDER = [
    "Mean", "Variance", "Standard Deviation", "Entropy", "Skewness",
    "Kurtosis", "Contrast", "Energy", "ASM", "Homogeneity",
    "Dissimilarity", "Correlation", "Coarseness",
]

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="Brain Tumor MRI Classifier", page_icon="🧠")

st.title("🧠 Brain Tumor MRI Classifier")

st.write(
    "Upload a brain MRI image (PNG/JPG). The model extracts texture features "
    "(GLCM + statistical) and predicts tumor presence using a tuned Random Forest."
)

# -------------------------------------------------
# Upload image
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Choose an MRI image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    st.image(uploaded_file, caption="Uploaded MRI", width=300)

    # Temporary file
    temp_path = ROOT / "temp_upload.png"

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract features
    features = extract_features(str(temp_path))

    feature_df = pd.DataFrame(
        [[features[f] for f in FEATURE_ORDER]],
        columns=FEATURE_ORDER
    )

    # Prediction
    prediction = model.predict(feature_df)[0]
    proba = model.predict_proba(feature_df)[0]

    st.subheader("Result")

    if prediction == 1:
        confidence = proba[1] * 100
        st.error(f"⚠️ Tumor Detected (confidence: {confidence:.2f}%)")
    else:
        confidence = proba[0] * 100
        st.success(f"✅ No Tumor Detected (confidence: {confidence:.2f}%)")

    # Show extracted features
    with st.expander("See extracted features"):
        st.dataframe(
            feature_df.T.rename(columns={0: "Value"})
        )

st.caption(
    "Disclaimer: Educational/portfolio project only — not a medical diagnostic tool."
)