#Writing inference schema to generate Swagger documentation automatically

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.standard_py_parameter_type import (
    StandardPythonParameterType
)
import os
import numpy as np
import logging
import joblib
import json
import uuid
import pandas as pd

model = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)
service_name = None

def init():
    global model, service_name
    service_name = "online/" + os.getenv("AZUREML_MODEL_DIR").split('/', 4)[-1]
    model_dir = os.getenv('AZUREML_MODEL_DIR', '')
    model_path = os.path.join(model_dir, 'model_pipeline', 'model.pkl')
    model = joblib.load(model_path)
    logger.info(json.dumps({
        "service_name": service_name,
        "type": "InitializeService",
    }))

@input_schema(
    param_name = 'data', param_type = StandardPythonParameterType([[63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 'fixed']])
)
@output_schema(output_type=StandardPythonParameterType({'Disease': ['Yes']}))
def run(data):
    try:
        global model
        request_id = uuid.uuid4().hex
        ip_features = ['age', 'chol', 'oldpeak', 'thalach', 'trestbps', 'ca', 'cp', 'exang',
       'fbs', 'restecg', 'sex', 'slope', 'thal']
        input_df = pd.DataFrame(data, columns = ip_features)
        predictions = model.predict(input_df)
        targets = ['Yes', 'No']
        predicted_categories = np.choose(predictions, targets).flatten()
        result = {
            "Disease": predicted_categories.tolist(),
        }
        predictions = predictions.tolist()
        
        # Log input data
        logger.info(json.dumps({
            "service_name": service_name,
            "type": "InputData",
            "request_id": request_id,
            "data": input_df.to_json(orient='records'),
        }))
        logger.info(json.dumps({
            "service_name": service_name,
            "type": "OutputData",
            "request_id": request_id,
            "data": predictions
        }))
        return result
    except Exception as error:
        logger.error(json.dumps({
            "service_name": service_name,
            "type": "Exception",
            "request_id": request_id,
            "error": error
        }), exc_info=error)