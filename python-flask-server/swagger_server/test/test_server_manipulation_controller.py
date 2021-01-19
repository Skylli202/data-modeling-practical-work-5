# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestServerManipulationController(BaseTestCase):
    """ServerManipulationController integration test stubs"""

    def test_create(self):
        """Test case for create

        Create a server from last ontology file
        """
        response = self.client.open(
            '/api/create',
            method='POST',
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_from_file(self):
        """Test case for create_from_file

        Create a server with an owl file
        """
        data = dict(ontology=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/create_from_file',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete(self):
        """Test case for delete

        Delete all data
        """
        response = self.client.open(
            '/api/delete',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_dataset(self):
        """Test case for get_dataset

        get the owl file corresponding to the dataset
        """
        response = self.client.open(
            '/api/getDataset',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_query(self):
        """Test case for send_query

        Send a sparql query to the server
        """
        query_string = [('query', 'query_example')]
        response = self.client.open(
            '/api/query',
            method='GET',
            content_type='text/plain; charset=utf-8',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_stop(self):
        """Test case for stop

        Stop the server
        """
        response = self.client.open(
            '/api/stop',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update(self):
        """Test case for update

        Send a sparql to update the ontology
        """
        query_string = [('query', 'query_example')]
        response = self.client.open(
            '/api/update',
            method='POST',
            content_type='text/plain; charset=utf-8',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
