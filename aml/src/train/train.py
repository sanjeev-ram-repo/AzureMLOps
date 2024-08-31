
import argparse
import os
import sys
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, matthews_corrcoef
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import mlflow
from mlflow.models.signature import infer_signature

def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str)
    parser.add_argument('--target_column', type=str, default = 'target')
    parser.add_argument('--feat_transformer', type=str)
    parser.add_argument('--model_name', type=str, default = 'best_model')
    parser.add_argument('--max_depth', type=int, default = 3)
    parser.add_argument('--scale_pos_weight', type=int, default = 99)
    parser.add_argument('--model_folder', type=str)
    return parser.parse_args()

def train_model(feat_transformer, params, train_features, train_target):
    transformations = mlflow.sklearn.load_model(feat_transformer)
    pipeline = Pipeline(steps=[('transformer', transformations),
                              ('xgbc', XGBClassifier(**params))
                    ])
    pipeline.fit(train_features, train_target)
    return pipeline

def main(args):
    try:
        with mlflow.start_run(nested=True):

            params = {'max_depth':args.max_depth, 
                      'scale_pos_weight': args.scale_pos_weight
            }

            mlflow.xgboost.autolog(log_models=False)
            
            train = pd.read_csv(Path(args.data) / 'train.csv')
            test = pd.read_csv(Path(args.data) / 'test.csv')
            
            train_features = train.drop(columns=[args.target_column])
            train_target = train[args.target_column]

            model = train_model(args.feat_transformer, params, 
                                train_features, train_target)
            
            test_features = test.drop(columns=[args.target_column])
            test_target = test[args.target_column]
            
            predictions = model.predict(test_features)
            accuracy = accuracy_score(test_target, predictions)
            recall = recall_score(test_target, predictions)
            matthews_corr = matthews_corrcoef(test_target, predictions)
            mlflow.log_metrics({'accuracy': accuracy, 'recall': recall,
                                 'mathews_coref' : matthews_corr})
            
            mlflow.sklearn.save_model(model, path = str(Path(args.model_folder)))
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)

if __name__ == '__main__':
    args = parser_args()
    main(args)