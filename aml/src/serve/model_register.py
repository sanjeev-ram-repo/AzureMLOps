

import argparse
import mlflow
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import skl2onnx
from skl2onnx.common.shape_calculator import calculate_linear_classifier_output_shapes
from skl2onnx.common.data_types import FloatTensorType, Int64TensorType, StringTensorType
from onnxmltools.convert.xgboost.operator_converters.XGBoost import convert_xgboost


parser = argparse.ArgumentParser()

parser.add_argument('--data', type=str)
parser.add_argument('--model_path', type=str)
parser.add_argument('--model_pipeline', type=str)
args = parser.parse_args()


model = mlflow.sklearn.load_model(args.model_path)


mlflow.sklearn.save_model(model, path = args.model_pipeline)
mlflow.sklearn.log_model(model, registered_model_name = 'heart_disease_prediction_model', artifact_path = args.model_pipeline)
