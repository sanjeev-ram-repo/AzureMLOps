import os
import json
import logging
import argparse
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import (CatTargetDriftProfileSection,
                                              DataDriftProfileSection)
from evidently.pipeline.column_mapping import ColumnMapping
from opencensus.ext.azure.log_exporter import AzureLogHandler

continuous_features = ['age', 'chol', 'oldpeak', 'thalach', 'trestbps']
discrete_features = ['ca', 'cp', 'exang', 'fbs', 'restecg', 'sex', 'slope', 'thal']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--reference_data", type=str)
    parser.add_argument("--target_data", type=str)
    return parser.parse_args()

def get_latest_file(dir):
    files = sorted(os.listdir(dir))[::-1] #Picking the latest file
    if files:
        return f'{dir}/{files[-1]}'


def process_data_drift_output(data_drift_metrics):
    overall_metrics = {
        "n_features": data_drift_metrics["n_features"],
        "n_drifted_features": data_drift_metrics["n_drifted_features"],
        "share_drifted_features": data_drift_metrics["share_drifted_features"],
        "dataset_drift": data_drift_metrics["dataset_drift"]
    }

    # define feature data drift metrics table
    feature_metrics = []

    # preprocess json output
    for feature in [*continuous_features, *discrete_features]:
        feature_metrics.append({
            "feature_name": feature,
            "drift_score": data_drift_metrics[feature]["drift_score"],
            "drift_detected": data_drift_metrics[feature]["drift_detected"],
            "feature_type": data_drift_metrics[feature]["feature_type"],
            "stattest_name": data_drift_metrics[feature]["stattest_name"],
        })

    return overall_metrics, feature_metrics

def main(args, log):
    try:
        reference = pd.read_csv(args.reference_data)
        target = pd.read_csv(get_latest_file(args.target_data))
        #target_column = 'target'
        reference[discrete_features] = reference[discrete_features].astype(
            "str")
        reference[continuous_features] = reference[continuous_features].astype(
            "float")
        target[discrete_features] = target[discrete_features].astype(
            "str")
        target[continuous_features] = target[continuous_features].astype(
            "float")
        
        column_mapping = ColumnMapping()
        column_mapping.target = None
        column_mapping.prediction = None
        column_mapping.id = None
        column_mapping.datetime = None
        column_mapping.numerical_features = continuous_features
        column_mapping.categorical_features = discrete_features

        data_drift_profile = Profile(
            sections=[DataDriftProfileSection(),
                      CatTargetDriftProfileSection()])
        data_drift_profile.calculate(
            reference, target, column_mapping=column_mapping)

        # convert drift  profile to json
        data_drift_profile_json = json.loads(data_drift_profile.json())
        print(data_drift_profile_json)

        # process data drift output
        overall_metrics, feature_metrics = process_data_drift_output(
            data_drift_profile_json["data_drift"]["data"]["metrics"])

        print("Overall data drift metrics:", overall_metrics)
        print("Feature data drift metrics:", feature_metrics)

        # Log overall drift metrics
        log.info(json.dumps({
            "model_name": args.model_name,
            "type": "OverallDriftMetrics",
            "data": overall_metrics
        }))

        # Log feature drift metrics
        log.info(json.dumps({
            "model_name": args.model_name,
            "type": "FeatureDriftMetrics",
            "data": feature_metrics
        }))

    except Exception as e:
        log.error(json.dumps({
            "model_name": args.model_name,
            "type": "Exception",
            "error": e
        }), exc_info=e)
    
if __name__ == "__main__":
    args = parse_args()
    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    logger.addHandler(AzureLogHandler())
    main(args, logger)