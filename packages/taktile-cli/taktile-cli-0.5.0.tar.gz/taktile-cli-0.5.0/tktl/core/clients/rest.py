import json
import os
from typing import Optional

from openapi_schema_pydantic import OpenAPI  # type: ignore

from tktl.core.clients import Client
from tktl.core.clients.http_client import API, interpret_response
from tktl.core.config import settings
from tktl.core.exceptions.exceptions import APIClientException
from tktl.core.loggers import LOG, Logger
from tktl.core.schemas.repository import _format_http_url
from tktl.core.t import ServiceT


class RestClient(Client):
    def get_schema(self, *args, **kwargs):
        pass

    TRANSPORT = ServiceT.REST

    def __init__(
        self,
        api_key: str,
        repository_name: str,
        branch_name: str,
        endpoint_name: str,
        local: bool = False,
        logger: Logger = LOG,
        verbosity: int = 0,
        skip_auth: bool = False,
    ):
        super().__init__(
            api_key=api_key,
            repository_name=repository_name,
            branch_name=branch_name,
            endpoint_name=endpoint_name,
            local=local,
            logger=logger,
            verbosity=verbosity,
        )
        if not skip_auth:
            self._authenticate()

    def predict(self, inputs):
        response = self.client.post(
            url=f"model/{self.endpoint_name}", data=json.dumps(inputs)
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def for_url(cls, api_key: str, url: str, endpoint_name: str):
        rest_url = cls.format_url(url=url)
        instantiated = cls(
            api_key=api_key,
            repository_name="",
            branch_name="",
            endpoint_name=endpoint_name,
            skip_auth=True,
        )
        client = API(api_url=rest_url)
        instantiated.set_client_and_location(location=rest_url, client=client)
        instantiated.logger.trace(f"Performing authentication request against {url}")
        try:
            instantiated.health()
        except APIClientException as e:
            instantiated.logger.error(f"Could not instantiate client: {e.detail}")
            return
        return instantiated

    @staticmethod
    def format_url(url: Optional[str]) -> str:
        return _format_http_url(url, docs=False)

    def _authenticate(self, health_check: bool = False):
        if health_check:
            location = self.get_deployment_location()
        else:
            location = self.get_endpoint_and_location()
        client = API(api_url=location)
        self.set_client_and_location(location=location, client=client)

    @property
    def local_endpoint(self):
        return settings.LOCAL_REST_ENDPOINT

    def list_deployments(self):
        pass

    def get_sample_data(self):
        if not self.endpoint_has_rest_sample_data:
            self.logger.warning("Sample data not available for this endpoint")
            return None, None
        schema = self.client.get(url="openapi.json")
        openapi = OpenAPI.parse_obj(schema.json())
        request_reference, response_reference = get_endpoint_model_reference(
            openapi, endpoint=self.endpoint_name
        )
        sample_input = openapi.components.schemas[request_reference].example
        if not sample_input:
            self.logger.warning("No sample input found for endpoint")
        sample_output = openapi.components.schemas[response_reference].example
        if not sample_output:
            self.logger.warning("No sample output found for endpoint")
        return sample_input, sample_output

    def health(self):
        response = self.client.get(url="openapi.json")
        return interpret_response(response, model=None, ping=True)


def get_endpoint_model_reference(openapi: OpenAPI, endpoint: str):
    for k in openapi.paths.keys():
        if f"/model/{endpoint}" == k:
            request_ref = (
                openapi.paths[k]
                .post.requestBody.content["application/json"]
                .media_type_schema.ref
            )
            response_ref = (
                openapi.paths[k]
                .post.responses["200"]
                .content["application/json"]
                .media_type_schema.ref
            )
            return os.path.basename(request_ref), os.path.basename(response_ref)
    return None
