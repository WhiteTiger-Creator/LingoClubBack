import json
import os
from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectTimeout


class ClientBase:
    """
    This is a wrapper of the python module of requests.
    """

    def __init__(self, host, port, path, protocol="http"):
        self.protocol = protocol
        self.host = host
        self.port = port
        if path and path[0] != "/":
            self.path = "/" + path
        else:
            self.path = path
        self.target_url = None
        self.headers = {}
        self.queries = {}
        self.payload = None  # The payload on the request
        self.request_timeout = 10  # in seconds
        self.proxy = None  # set proxy if proxy is needed
        self.trusted_ca = None  # Add a trusted ca file and save it here.
        self.action = None

    def build_target_url(self):
        """Build target url"""
        if self.port:
            self.target_url = f"{self.protocol}://{self.host}:{self.port}{self.path}"
        else:
            self.target_url = f"{self.protocol}://{self.host}{self.path}"
        if self.queries:
            self.target_url += "?"
            self.target_url += urlencode(self.queries)

    def add_header(self, key, value):
        """Add a header to the client"""
        if key not in self.headers:
            self.headers[key] = value

    def add_trusted_ca_file_path(self, trusted_ca_file_path):
        """Add a trusted ca file path"""
        if not os.path.isfile(trusted_ca_file_path):
            raise RuntimeError(f"{trusted_ca_file_path} does not exist.")
        self.trusted_ca = trusted_ca_file_path

    def add_proxy(self, proxy):
        """Add a proxy instance"""
        self.proxy = proxy.build()

    def append_path(self, path):
        if self.path:
            self.path += path
        else:
            self.path = path

    def add_payload(self, payload: dict):
        """
        Add a python object as the payload.
        """
        self.payload = json.dumps(payload)
        print(self.payload)

    def add_query(self, key: str, value: str):
        """Add a query to target url"""
        self.queries[key] = value

    def build_request_param(self):
        data = {"headers": self.headers, "timeout": self.request_timeout}
        if self.proxy:
            data["proxies"] = self.proxy
        if self.trusted_ca:
            data["verify"] = self.trusted_ca
        if self.payload:
            data["data"] = self.payload
        return data

    def _post_response_helper(self):
        params = self.build_request_param()
        return requests.post(self.target_url, **params)

    def _get_response_helper(self):
        params = self.build_request_param()
        return requests.get(self.target_url, **params)

    def _put_response_helper(self):
        params = self.build_request_param()
        return requests.put(self.target_url, **params)

    def _delete_response_helper(self):
        params = self.build_request_param()
        return requests.delete(self.target_url, **params)

    def retrieve_post_response(self):
        """Get the server response for the HTTP action POST"""
        self.action = "POST"
        return self.retrieve_response()

    def retrieve_get_response(self):
        """Get the server response for the HTTP action GET"""
        self.action = "GET"
        return self.retrieve_response()

    def retrieve_delete_response(self):
        """Get the server response for the HTTP action DELETE"""
        self.action = "DELETE"
        return self.retrieve_response()

    def retrieve_put_response(self):
        """Get the server response for the HTTP action PUT"""
        self.action = "PUT"
        return self.retrieve_response()

    def retrieve_response(self):
        self.build_target_url()
        params = self.build_request_param()
        try:
            if self.action == "GET":
                response = requests.get(self.target_url, **params)
            elif self.action == "POST":
                response = requests.post(self.target_url, **params)
            elif self.action == "PUT":
                response = requests.put(self.target_url, **params)
            elif self.action == "DELETE":
                response = requests.delete(self.target_url, **params)
            elif self.action == "PATCH":
                response = requests.patch(self.target_url, **params)
            else:
                raise Exception(f"action={self.action} is not implemented yet.")
            if response.status_code >= 400:
                raise RuntimeError(f'errorCode={response.status_code} errorMessage={response.content} url={self.target_url}')
        except ConnectTimeout:
            raise RuntimeError(f'ConnectTimeout: url={self.target_url}')
        return response

    def dry_run(self):
        self.build_target_url()
        cmd = f"curl -X {self.action} {self.target_url}"
        if self.payload:
            cmd += f" --data '{self.payload}'"
        if self.headers:
            for key in self.headers:
                cmd += f" -H '{key}:{self.headers[key]}'"
        return cmd
