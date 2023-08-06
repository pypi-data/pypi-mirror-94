from typing import List
from typing import Optional
from typing import Union

from cleaninsights.campaign import Campaign
from cleaninsights.conf import Configuration
from cleaninsights.store import Store


class CleanInsights:
    conf: Configuration
    store: Store
    persistence_counter: int

    def __init__(self, conf, store):
        self.conf = conf
        self.store = store

    def measure_visit(self, path: str, campaign_id: str):
        raise NotImplementedError

    def measure_event(self, category: str,
                      action: str,
                      campaign_id: str,
                      name: Optional[str] = None,
                      value: Union[int, float] = None):
        raise NotImplementedError

    @property
    def feature_consents(self) -> List[str]:
        raise NotImplementedError

    @property
    def campaign_consents(self) -> List[str]:
        raise NotImplementedError

    def feature_consent_by_index(self, index: int):
        raise NotImplementedError

    def campaign_consent_by_index(self, index: int):
        raise NotImplementedError

    def grant_feature(self, feature):
        raise NotImplementedError

    def deny_feature(self, feature):
        raise NotImplementedError

    def grant_campaign(self, campaign_id: str):
        raise NotImplementedError

    def deny_campaign(self, campaign_id: str):
        raise NotImplementedError

    def is_campaign_currently_granted(self, campaign_id: str) -> bool:
        raise NotImplementedError

    def persist(self) -> None:
        raise NotImplementedError

    def get_campaign_if_good(self, campaign_id: str,
                             debug_str: str) -> Optional[Campaign]:
        raise NotImplementedError
