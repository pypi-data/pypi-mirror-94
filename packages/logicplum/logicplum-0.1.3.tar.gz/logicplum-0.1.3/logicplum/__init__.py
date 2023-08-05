import requests
import pandas as pd

from . import config


class LogicPlum:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_project(self, name, description):
        url = f"{config.HOST_NAME}{config.PROJECT_CREATE}"

        headers = {
            'Authorization': self.api_key
        }

        data = {
            'name': name,
            'description': description,
        }

        response = requests.post(url, data=data, headers=headers).json()

        if 'error' in response:
            return response['error']

        return response['project_id']


    def train(self, project_id, df, target):
        url = f"{config.HOST_NAME}{config.MODEL_TRAIN}"

        headers = {
            'Authorization': self.api_key
        }

        json_df = df.to_json(orient='records')

        data = {
            'project_id': project_id,
            'target': target,
            'data': json_df,
        }

        response = requests.post(url, data=data, headers=headers).json()

        return response

    def train_status(self, project_id):
        url = f"{config.HOST_NAME}{config.MODEL_TRAIN_STATUS}"

        headers = {
            'Authorization': self.api_key
        }

        params = {
            'project_id': project_id,
        }

        response = requests.get(url, params=params, headers=headers).json()

        return response


    def score(self, deployment_id, df):
        url = f"{config.HOST_NAME}{config.MODEL_SCORE}"

        headers = {
            'Authorization': self.api_key
        }

        json_df = df.to_json(orient='records')

        data = {
            'deployment_id': deployment_id,
            'data': json_df,
        }

        response = requests.post(url, data=data, headers=headers).json()
        if 'error' in response:
            return response['error']

        return pd.read_json(response['prediction'], orient='records')
