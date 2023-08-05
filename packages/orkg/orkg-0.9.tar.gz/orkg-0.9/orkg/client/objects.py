from orkg.utils import NamespacedClient, query_params
from orkg.out import OrkgResponse
from pandas import read_csv
import re
from ast import literal_eval
import os


class ObjectsClient(NamespacedClient):

    def add(self, params=None):
        """
        Warning: Super-users only should use this endpoint
        Create a new object in the ORKG instance
        :param params: orkg Object
        :return: an OrkgResponse object containing the newly created object resource
        """
        self.client.backend._append_slash = True
        response = self.client.backend.objects.POST(json=params, headers=self.auth)
        return OrkgResponse(response)

