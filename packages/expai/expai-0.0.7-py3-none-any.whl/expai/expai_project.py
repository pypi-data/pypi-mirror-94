import requests
import logging
from expai.expai_model import ExpaiModelExplainer


class ExpaiProject:
    def __init__(self, project_id: str, api_key: str, headers: dict, server_name: str, session):

        self.project_id = project_id

        self.server_name = server_name
        self.api_key = api_key

        self.headers = headers
        
        self.sess = session

    #########################
    ###      MODELS       ###
    #########################

    def model_list(self):
        """
        List all models within the project
        :return: list of models
        """
        response = self.sess.request("GET", self.server_name + "/api/projects/{}/model/list".format(self.project_id),
                                    headers=self.headers)
        if response.ok:
            return response.json()['models']
        else:
            logging.error("There was an error listing your models. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def create_model(self, model_path: str = None, is_supervised: bool = True, model_name: str = None,
                     model_type: str = None, model_library: str = None, model_objective: str = None):
        """
        Create a new model for a project.
        :param model_path: path where your model is stored locally
        :param is_supervised: Indicate whether the model is supervised
        :param model_name: Name you want to give to the model
        :return: True if successful
        """
        assert model_name is not None, "To create a model you must give it a model_name"
        assert model_path is not None, "To create a model you must specify the path to the stored model"
        assert model_type is not None, "Please, indicate the model_type. Refer to documentation for further information"
        assert model_library is not None, "Please, indicate the model_library. Refer to documentation for further information"
        assert model_objective is not None, "Please, indicate the model_objective. Refer to documentation for further information"


        data = {"model_name_des": model_name,
                "is_supervised_flag": 1 if is_supervised else 0,
                'model_type_des': model_type,
                'model_library_des': model_library,
                'model_objective_des': model_objective}

        files = {'model_file': open(model_path, 'rb')}
        headers = {'api_key': self.api_key}

        response = self.sess.request("GET", self.server_name + "/api/projects/{}/model/create".format(self.project_id),
                                    data=data, headers=headers, files=files)

        if response.ok:
            return True
        else:
            logging.error("There was an error creating the model. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def delete_model(self, model_name: str = None, model_id: str = None):
        """
        Delete a model within a project
        :param model_name: name of the model you want to remove
        :param model_id: Id for the model you want to remove (optional)
        :return: True if successful
        """
        assert model_id is not None or model_name is not None, "You must indicate the model_name or model_id"

        if model_id is None:
            model_id = self._get_model_id_from_name(model_name)

        response = self.sess.request("DELETE",
                                    self.server_name + "/api/projects/{}/model/{}".format(self.project_id, model_id),
                                    headers=self.headers)

        if response.ok:
            return True
        else:
            logging.error("There was an error deleting the model. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def get_model_explainer(self, model_name: str = None, model_id: str = None):
        """
        Get a Python object that will enable you to interact with a project and its models.
        :param model_name: Name of the project
        :param model_id: Id of the project (optional)
        :return: ExpaiModel object
        """
        assert model_name is not None or model_id is not None, "You must provide a project name or project id"

        if model_id is None:
            model_id = self._get_model_id_from_name(model_name)

        if model_id is not None:
            return ExpaiModelExplainer(model_id, self.project_id, self.api_key, self.headers, self.server_name, self.sess, self)
        else:
            logging.error("We could not find your model. Please, check your name or try using model_id as parameter")

    def _get_model_id_from_name(self, model_name: str = None):

        model_list = self.model_list()
        if model_list is None:
            raise Exception('Model not found')
        for model in model_list:
            if model['model_name_des'] == model_name:
                return model['model_id']
        return None

    #########################
    ###      SAMPLES      ###
    #########################

    def sample_list(self):
        """
        List all samples associated with this project
        :return: list of samples
        """
        response = self.sess.request("GET", self.server_name + "/api/projects/{}/sample/list".format(self.project_id),
                                    headers=self.headers)

        if response.ok:
            return response.json()['samples']
        else:
            logging.error("There was an error listing your samples. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def create_sample(self, sample_path: str = None, sample_name: str = None, sample_separator: str = None, sample_target_col: str = None,
                      sample_encoding: str = 'utf-8'):
        """
        Create a new sample for the project
        :param sample_target_col: target column for the model
        :param sample_path: local path to the stored file
        :param sample_name: name for your new file
        :param sample_separator: separator for the sample columns
        :param sample_encoding: encoding of the file (optional). Default: utf-8.
        :return: True if successful
        """
        assert sample_name is not None, "To create a sample you must give it a sample_name"
        assert sample_path is not None, "To create a sample you must specify the path to the stored file"
        assert sample_separator is not None, "Please, specify the file separator"
        assert sample_target_col is not None, "Please, specify a target column"


        data = {"sample_name_des": sample_name,
                "sample_file_separator_des": sample_separator,
                "sample_file_encoding_des": sample_encoding,
                "sample_target_col": sample_target_col}

        files = {'sample_file': open(sample_path, 'r')}

        headers = {'api_key': self.api_key}

        response = self.sess.request("GET", self.server_name + "/api/projects/{}/sample/create".format(self.project_id),
                                    data=data, headers=headers, files=files)

        if response.ok:
            return True
        else:
            logging.error("There was an error creating the model. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def delete_sample(self, sample_name: str = None, sample_id: str = None):
        """
        Delete a model within a project
        :param model_name: name of the model you want to remove
        :param model_id: Id for the model you want to remove (optional)
        :return: True if successful
        """
        assert sample_id is not None or sample_name is not None, "You must indicate the model_name or model_id"

        if sample_id is None:
            sample_id = self._get_sample_id_from_name(sample_name)

            if sample_id is None:
                logging.error(
                    "We could not find any sample matching that name. Please, try again or use sample_id as parameter")
                return False

        response = self.sess.request("DELETE",
                                    self.server_name + "/api/projects/{}/sample/{}".format(self.project_id, sample_id),
                                    headers=self.headers)

        if response.ok:
            return True
        else:
            logging.error("There was an error deleting the sample. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def _get_sample_id_from_name(self, sample_name: str = None):

        sample_list = self.sample_list()
        for sample in sample_list:
            if sample['sample_name_des'] == sample_name:
                return sample['sample_id']
        return None

