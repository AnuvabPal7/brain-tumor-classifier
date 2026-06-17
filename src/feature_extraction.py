import numpy as np
from PIL import Image
from skimage.feature import graycomatrix, graycoprops
from scipy.stats import skew, kurtosis


def extract_features(image_path):
    """
    Extract first-order statistical features and GLCM texture features
    from a grayscale image, matching the columns used in Brain Tumor.csv:
    Mean, Variance, Standard Deviation, Entropy, Skewness, Kurtosis,
    Contrast, Energy, ASM, Homogeneity, Dissimilarity, Correlation, Coarseness
    """
    # Load image and convert to grayscale
    img = Image.open(image_path).convert("L")
    img = img.resize((256, 256))  # standardize size
    arr = np.array(img, dtype=np.float64)
    flat = arr[arr > 0]

    # First-order statistics
    mean = np.mean(flat)
    variance = np.var(flat)
    std_dev = np.std(flat)

    # Entropy (based on histogram)
    hist, _ = np.histogram(flat, bins=256, range=(0, 256), density=True)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))

    skewness = skew(flat)
    kurt = kurtosis(flat)

    # GLCM texture features (using uint8 image)
    arr_uint8 = arr.astype(np.uint8)
    glcm = graycomatrix(
        arr_uint8,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True,
    )

    contrast = graycoprops(glcm, "contrast")[0, 0]
    energy = graycoprops(glcm, "energy")[0, 0]
    asm = graycoprops(glcm, "ASM")[0, 0]
    homogeneity = graycoprops(glcm, "homogeneity")[0, 0]
    dissimilarity = graycoprops(glcm, "dissimilarity")[0, 0]
    correlation = graycoprops(glcm, "correlation")[0, 0]

    # Coarseness - simple approximation (average absolute gradient)
    grad_x = np.abs(np.diff(arr, axis=1))
    grad_y = np.abs(np.diff(arr, axis=0))
    coarseness = 1.0 / (np.mean(grad_x) + np.mean(grad_y) + 1e-10)

    features = {
        "Mean": mean,
        "Variance": variance,
        "Standard Deviation": std_dev,
        "Entropy": entropy,
        "Skewness": skewness,
        "Kurtosis": kurt,
        "Contrast": contrast,
        "Energy": energy,
        "ASM": asm,
        "Homogeneity": homogeneity,
        "Dissimilarity": dissimilarity,
        "Correlation": correlation,
        "Coarseness": coarseness,
    }

    return features