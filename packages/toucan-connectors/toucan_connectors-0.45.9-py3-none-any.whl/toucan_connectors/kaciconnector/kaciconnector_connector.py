import pandas as pd

from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource


class KaciconnectorDataSource(ToucanDataSource):
    query: str


class KaciconnectorConnector(ToucanConnector):
    data_source_model: KaciconnectorDataSource

    username: str
    password: str

    def _retrieve_data(self, data_source: KaciconnectorDataSource) -> pd.DataFrame:
        pass
