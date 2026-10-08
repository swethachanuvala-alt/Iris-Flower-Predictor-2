"""Training pipeline for the Iris app.

It mirrors the steps in notebooks/GGST__2.ipynb:
  1. drop Id / empty column, fill missing values (median / mode)
  2. label-encode Species
  3. 80/20 split (random_state=42)
  4. StandardScaler fitted on the training split
  5. balance the training split with SMOTE-style oversampling
  6. Decision Tree with the best parameters found by GridSearchCV
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Iris.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_FILE = MODEL_DIR / "Decision_Tree_model.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"
ENCODER_FILE = MODEL_DIR / "label_encoders.pkl"
META_FILE = MODEL_DIR / "metadata.json"

FEATURES = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
TARGET = "Species"
SHORT = {
    "SepalLengthCm": "Sepal length",
    "SepalWidthCm": "Sepal width",
    "PetalLengthCm": "Petal length",
    "PetalWidthCm": "Petal width",
}
CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]

# Best parameters found by GridSearchCV in the notebook
BEST_PARAMS = dict(criterion="gini", max_depth=None, min_samples_leaf=4,
                   min_samples_split=2, random_state=42)


# ----------------------------------------------------------------- data
def load_raw() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    drop = [c for c in df.columns if c == "Id" or str(c).startswith("Unnamed")]
    return df.drop(columns=drop)


def load_notebook_frame() -> pd.DataFrame:
    """Same cleaning as the notebook (fills the blank last row with median/mode)."""
    df = load_raw()
    for col in FEATURES:
        df[col] = df[col].fillna(df[col].median())
    df[TARGET] = df[TARGET].fillna(df[TARGET].mode()[0])
    return df


def load_plot_frame() -> pd.DataFrame:
    """The 150 real flowers with friendly species names (for charts)."""
    df = load_raw().dropna().reset_index(drop=True)
    df[TARGET] = df[TARGET].str.replace("Iris-", "", regex=False).str.capitalize()
    return df


# ------------------------------------------------------------ modelling
def smote_balance(X, y, k: int = 5, random_state: int = 42):
    """Small SMOTE implementation (so the app needs no imbalanced-learn)."""
    rng = np.random.RandomState(random_state)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    classes, counts = np.unique(y, return_counts=True)
    target = counts.max()
    X_out, y_out = [X], [y]
    for cls, n in zip(classes, counts):
        need = int(target - n)
        if need <= 0 or n < 2:
            continue
        Xc = X[y == cls]
        kk = min(k, len(Xc) - 1)
        nn = NearestNeighbors(n_neighbors=kk + 1).fit(Xc)
        idx = nn.kneighbors(Xc, return_distance=False)
        base = rng.randint(0, len(Xc), need)
        neigh = idx[base, rng.randint(1, kk + 1, need)]
        gap = rng.rand(need, 1)
        X_out.append(Xc[base] + gap * (Xc[neigh] - Xc[base]))
        y_out.append(np.full(need, cls))
    return np.vstack(X_out), np.concatenate(y_out)


def prepare():
    df = load_notebook_frame()
    encoder = LabelEncoder()
    y = encoder.fit_transform(df[TARGET])
    X = df[FEATURES]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler().fit(X_train)
    return dict(encoder=encoder, X_train=X_train, X_test=X_test,
                y_train=y_train, y_test=y_test, scaler=scaler,
                X_train_scaled=scaler.transform(X_train),
                X_test_scaled=scaler.transform(X_test))


def fit_model(data):
    Xr, yr = smote_balance(data["X_train_scaled"], data["y_train"])
    return DecisionTreeClassifier(**BEST_PARAMS).fit(Xr, yr)


def evaluate(model, X_test_scaled, y_test) -> dict:
    pred = model.predict(X_test_scaled)
    labels = [0, 1, 2]
    return dict(
        accuracy=float(accuracy_score(y_test, pred)),
        precision=float(precision_score(y_test, pred, average="weighted", zero_division=0)),
        recall=float(recall_score(y_test, pred, average="weighted", zero_division=0)),
        f1=float(f1_score(y_test, pred, average="weighted", zero_division=0)),
        confusion=confusion_matrix(y_test, pred, labels=labels).tolist(),
        report=classification_report(y_test, pred, labels=labels,
                                     target_names=CLASS_NAMES,
                                     output_dict=True, zero_division=0),
        n_test=int(len(y_test)),
    )


def train_fresh() -> dict:
    data = prepare()
    model = fit_model(data)
    return dict(model=model, scaler=data["scaler"], encoder=data["encoder"],
                data=data, source="trained from data/Iris.csv")


def save_artifacts(bundle: dict) -> None:
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(bundle["model"], MODEL_FILE)
    joblib.dump(bundle["scaler"], SCALER_FILE)
    joblib.dump({TARGET: bundle["encoder"]}, ENCODER_FILE)
    d = bundle["data"]
    m = evaluate(bundle["model"], d["X_test_scaled"], d["y_test"])
    META_FILE.write_text(json.dumps(
        {"sklearn_version": sklearn.__version__, "test_accuracy": m["accuracy"]}, indent=2))


def get_bundle() -> dict:
    """Use the saved model when it is compatible, otherwise retrain (never fails)."""
    data = prepare()
    model, scaler, source = None, data["scaler"], ""
    try:
        meta = json.loads(META_FILE.read_text())
        if meta.get("sklearn_version") == sklearn.__version__:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                m = joblib.load(MODEL_FILE)
                s = joblib.load(SCALER_FILE)
            if (isinstance(m, DecisionTreeClassifier)
                    and getattr(m, "n_features_in_", 0) == len(FEATURES)
                    and getattr(s, "n_features_in_", 0) == len(FEATURES)):
                model, scaler = m, s
                source = "loaded from model/Decision_Tree_model.pkl"
    except Exception:
        model = None
    if model is None:
        scaler = data["scaler"]
        model = fit_model(data)
        source = "trained at start-up from data/Iris.csv"
    metrics = evaluate(model, scaler.transform(data["X_test"]), data["y_test"])
    return dict(model=model, scaler=scaler, data=data, metrics=metrics, source=source,
                n_train=int(len(data["y_train"])),
                importances=dict(zip(FEATURES, model.feature_importances_.tolist())))


# ----------------------------------------------------------- inference
def predict(bundle: dict, values) -> dict:
    """values = [sepal_len, sepal_wid, petal_len, petal_wid] in cm."""
    model, scaler = bundle["model"], bundle["scaler"]
    x = pd.DataFrame([list(values)], columns=FEATURES)
    xs = scaler.transform(x)
    proba = model.predict_proba(xs)[0]
    pred = int(model.classes_[int(np.argmax(proba))])
    t = model.tree_
    steps = []
    for n in model.decision_path(xs).indices:
        if t.children_left[n] == t.children_right[n]:
            continue  # leaf
        f = int(t.feature[n])
        thr_cm = float(t.threshold[n] * scaler.scale_[f] + scaler.mean_[f])
        steps.append(dict(feature=SHORT[FEATURES[f]], threshold=thr_cm,
                          left=bool(xs[0, f] <= t.threshold[n]), value=float(values[f])))
    return dict(pred=pred, proba=[float(p) for p in proba], steps=steps)


def tree_rules(bundle: dict) -> str:
    model, scaler, t = bundle["model"], bundle["scaler"], bundle["model"].tree_
    lines = []

    def rec(n, depth):
        pad = "|   " * depth
        if t.children_left[n] == t.children_right[n]:
            cls = int(model.classes_[int(np.argmax(t.value[n][0]))])
            lines.append(f"{pad}=> {CLASS_NAMES[cls]}  ({int(t.n_node_samples[n])} samples)")
            return
        f = int(t.feature[n])
        thr = t.threshold[n] * scaler.scale_[f] + scaler.mean_[f]
        name = SHORT[FEATURES[f]]
        lines.append(f"{pad}if {name} <= {thr:.2f} cm:")
        rec(t.children_left[n], depth + 1)
        lines.append(f"{pad}else:  # {name} > {thr:.2f} cm")
        rec(t.children_right[n], depth + 1)

    rec(0, 0)
    return "\n".join(lines)
