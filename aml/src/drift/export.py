import os
import argparse
from datetime import datetime, timedelta, timezone
import pandas as pd
from azure.identity import ManagedIdentityCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--model_version", type=str)
    parser.add_argument("--prepared_data_dir", type=str)
    parser.add_argument("--log_analytics_workspace_id", type=str)
    parser.add_argument("--n_days", type=int)
    args = parser.parse_args()
    return args

def query_workspace(client, lws_id, query, start, end):
    response = client.query_workspace(
        workspace_id=lws_id,
        query=query,
        timespan=(start, end)
    )
    if response.status == LogsQueryStatus.PARTIAL:
        error = response.partial_error
        data = response.partial_data
        print(f"Partial error: {error.message}")
    else:
        data = response.tables
    for table in data:
        df = pd.DataFrame(data=table.rows, columns=table.columns)
    final_res = []
    for value in df.ResponsePayload:
        final_res.extend(eval(value))
    df = pd.DataFrame(final_res)
    return df

def main(args):
    #https://stackoverflow.com/questions/77903906/how-to-give-an-azure-ml-compute-cluster-access-to-data-lake-gen2-storage
    #https://learn.microsoft.com/en-us/azure/machine-learning/how-to-monitor-online-endpoints?view=azureml-api-2
    #client_id = os.environ.get('DEFAULT_IDENTITY_CLIENT_ID')
    credential = ManagedIdentityCredential()
    client = LogsQueryClient(credential)

    end_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    start_time = (end_time - timedelta(minutes=15))

    log_analytics_query = f"""
        AmlOnlineEndpointConsoleLog
        | where Message has 'online/{args.model_name}/{args.model_version}' and Message has 'InputData'
        | project TimeGenerated, ResponsePayload=parse_json(trim("INFO:root:" , tostring(Message))).data
        | mv-expand ResponsePayload
    """
    df = query_workspace(client, args.log_analytics_workspace_id, log_analytics_query,
                         start_time, end_time)
    if not df.empty:
        file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        df.to_csv(f"{args.prepared_data_dir}/{file_name}.csv", index=False)
        #file_path = f"{args.prepared_data_dir}/heart-disease/inference/online"
        #os.makedirs(file_path, exist_ok=True)
        #print(f'{file_path}/{file_name}')
        df.to_csv(f"{args.prepared_data_dir}/{file_name}.csv", index=False)
        #print(os.listdir(f"{file_path}"))
    else:
        print('No data generated for this period!')



if __name__ == '__main__':
    args = parse_args()
    main(args)
