import logging
from typing import Dict, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.utils._client_config import Cluster
from cognite.well_model.model.model.well import Well
from cognite.well_model.model.model_utils import deserialize_model

logger = logging.getLogger("WellsAPI")


class WellsAPI:
    def __init__(self, wells_client: APIClient, project: str, cluster: Cluster):
        self.wells_client = wells_client
        self.project = project
        self.cluster = cluster

    @staticmethod
    def deserialize_well(well_dict: Dict) -> Optional[Well]:
        """
        deserialize a json dictionary to a Well object

        @param well_dict: key-word arguments to deserialize
        @return: Well object
        """
        well: Optional[Well] = None
        try:
            well = deserialize_model(
                model_data=well_dict,
                model_class=Well,
                path_to_item=[*well_dict],
                check_type=False,
                configuration=None,
                spec_property_naming=True,
            )
        except Exception as e:
            well_id = well_dict.get("id")
            logger.info(f"Well with the id: {well_id} could not parse due to: {e}")

        return well

    def get_by_id(self, well_id: int) -> Optional[Well]:
        """
        Get well from a cdf asset id

        @param well_id: cdf asset id
        @return: Well object
        """
        path: str = f"/{self.project}/wells/{well_id}?env={self.cluster}"
        response: Response = self.wells_client.get(url_path=path)
        well_data = response.json()
        return self.deserialize_well(well_data)
