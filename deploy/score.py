import json
import joblib
import os
import numpy as np

def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model_dir", "forecast_model.joblib")
    model = joblib.load(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)
        input_data = np.array(data["data"])
        prediction = model.predict(input_data)
        return json.dumps({"result": prediction.tolist()})
    except Exception as e:
        return json.dumps({"error": str(e)})