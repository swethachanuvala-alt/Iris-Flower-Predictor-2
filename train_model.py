"""Re-create the model files in model/  ->  python train_model.py"""
from irisgarden import pipeline as P

if __name__ == "__main__":
    bundle = P.train_fresh()
    P.save_artifacts(bundle)
    d = bundle["data"]
    m = P.evaluate(bundle["model"], d["X_test_scaled"], d["y_test"])
    print("Saved model files to:", P.MODEL_DIR)
    print(f"Train rows: {len(d['y_train'])}  Test rows: {m['n_test']}")
    print(f"Test accuracy : {m['accuracy']:.4f}")
    print(f"Test F1 score : {m['f1']:.4f}")
