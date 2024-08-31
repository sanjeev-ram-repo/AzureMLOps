"""
Data preparation step for the heart disease prediction a binary classification problem.
"""
import os
import sys
from pathlib import Path
import argparse
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (OrdinalEncoder, OneHotEncoder, StandardScaler)
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import mlflow
from mlflow.models.signature import infer_signature

continuous_features = ['age', 'chol', 'oldpeak', 'thalach', 'trestbps']
discrete_features = ['ca', 'cp', 'exang', 'fbs', 'restecg', 'sex', 'slope', 'thal']
target_column = 'target'

def parseArgs():
    """
        Parse arguments for the data preparation
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data', type = str)
    parser.add_argument('--categorical_encoding', type = str, required = False)
    parser.add_argument('--test_size', type = float, default = 0.3)
    parser.add_argument('--prepared_data', type = str)
    parser.add_argument('--transformations_output', type = str)
    parser.add_argument('--log_model', type = float, default = 1.0)
    return parser.parse_args()

def preprocessing_pipeline(cf, df, categorical_encoding = 'ordinal'): 
    """
        Encoding the categorical and continuous features for modeling.
        cf -> Continuous feat df -> discrete feat
    """
    try:
        if categorical_encoding == 'ordinal':
            cat_enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan)
        elif categorical_encoding == 'onehot':
            cat_enc = OneHotEncoder(handle_unknown="ignore")
        else:
            raise NotImplementedError('Possible values are ordinal or onehot')

        conti_feat_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy = 'median')),
            ('scaler', StandardScaler())
        ])

        disc_feat_pipeline = Pipeline([
            #('imputer', SimpleImputer(strategy = 'most_frequent')), -- does not work with ONNX
            ('encoder', cat_enc)

        ])

        transformations = ColumnTransformer([
            ('conti_feat_pipeline', conti_feat_pipeline, cf),
            ('disc_feat_pipeline', disc_feat_pipeline, df)
        ])
        return transformations
    
    except Exception as e:

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)


def main(args):
    try:
        raw = pd.read_csv(args.raw_data)
        train, test = train_test_split(raw, test_size = args.test_size,
                                       random_state = 42, stratify = raw.target)

        raw.to_csv(str(Path(args.prepared_data) / 'raw.csv'), index=False)
        train.to_csv(str(Path(args.prepared_data) / 'train.csv'), index=False)
        test.to_csv(str(Path(args.prepared_data) / 'test.csv'), index=False)

        if not args.categorical_encoding:
            args.categorical_encoding = 'ordinal'

        transformations = preprocessing_pipeline(continuous_features,
                                                 discrete_features,
                                                 args.categorical_encoding
                                                 )

        mlflow.sklearn.save_model(
            sk_model = transformations,
            path = str(Path(args.transformations_output)),
        )

        if args.log_model:

            mlflow.log_metric('Split ratio', args.test_size)
            mlflow.log_metric('Train shape', train.shape)
            mlflow.log_metric('Test shape', test.shape)
        
    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)

if __name__ == '__main__':
    args = parseArgs()
    with mlflow.start_run() as run_experiment:
        main(args)