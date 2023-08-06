import requests
import logging
from expai.expai_project import ExpaiProject


class ExpaiLogin:
    def __init__(self, email: str = None, user_pass: str = None, api_key: str = None):
        assert api_key is not None, "You must provide an api_key"
        assert email is not None, "Please, introduce your user id"
        assert user_pass is not None, "Please, introduce your password"

        self.server_name = "http://127.0.0.1:5000"
        self.api_key = api_key
        self.email = email

        self.headers = {
            'api_key': self.api_key,
            'Content-Type': 'application/json'
        }

        json = {
            "email_des": email,
            "password_des": user_pass
        }

        self.sess = requests.session()
        response = self.sess.post(self.server_name + "/api/auth/login", headers=self.headers, json=json)

        if not response.ok:
            logging.error("Invalid credentials, please check them and try again. Thank you.")

    def project_list(self):
        """
        Returns the list of projects for the user
        :return: list of projects
        """
        response = self.sess.request("GET", self.server_name + "/api/projects/list", headers=self.headers)
        if response.ok:
            return response.json()['projects']
        else:
            logging.error("There was an error listing your projects.")
            return None

    def search_project(self, search_by: str = None):
        """
        Search all projects containing a term
        :param search_by: query term
        :return: list of projects containing that term in the name
        """
        assert search_by is not None, "Please, introduce a term to search"

        response = self.sess.request("GET", self.server_name + "/api/projects/list/contains/{}".format(search_by),
                                     headers=self.headers)
        if response.ok:
            return response.json()['projects']
        else:
            logging.error("There was an error searching the project. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def create_project(self, project_name: str = None):
        """
        Create a new project
        :param project_id: Name for the project
        :return: True if successful
        """
        assert project_name is not None, "Please, introduce a project_id"

        payload = {"project_name_des": project_name}
        response = self.sess.request("GET", self.server_name + "/api/projects/create", headers=self.headers,
                                     json=payload)

        if response.ok:
            return True
        else:
            logging.error("There was an error creating the project. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def delete_project(self, project_name: str = None, project_id: str = None):
        """
        Delete a project. You must indicate project_id or project_name
        :param project_id: id for the project (optional).
        :param project_name: name of the project.
        :return:
        """
        assert project_id is not None or project_name is not None, "To delete a project you must specify its project_id or project_name"

        if project_id is None:
            project_id = self._get_project_id_from_name(project_name)

        response = self.sess.request("DELETE", self.server_name + "/api/projects/{}".format(project_id),
                                     headers=self.headers)

        if response.ok:
            return True
        else:
            logging.error("There was an error deleting the project. Please, check the details below. \n {}".format(
                response.json()['message']))
            return None

    def get_project(self, project_name: str = None, project_id: str = None):
        """
        Get a Python object that will enable you to interact with a project and its models.
        :param project_name: Name of the project
        :param project_id: Id of the project (optional)
        :return: ExpaiProject object
        """
        assert project_name is not None or project_id is not None, "You must provide a project name or project id"

        if project_id is None:
            project_id = self._get_project_id_from_name(project_name)

        if project_id is not None:
            return ExpaiProject(project_id, self.api_key, self.headers, self.server_name, self.sess)
        else:
            logging.error("We could not find your project. Please, check your name or try using project_id as parameter")
            return None

    def _get_project_id_from_name(self, project_name: str = None):
        project_list = self.search_project(search_by=project_name)

        for project in project_list:
            if project['project_name_des'] == project_name:
                return project['project_id']

        return None
