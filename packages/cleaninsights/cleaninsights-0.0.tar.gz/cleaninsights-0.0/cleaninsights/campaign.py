from dataclasses import dataclass
from datetime import date
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class Campaign:
    start: date
    end: date
    aggregation_period_length: int
    number_of_periods: Optional[int]
    only_record_once: bool
    event_aggregation_rule: str

    @classmethod
    def from_dict(cls, campaign_data: Dict[str, Any]):  # -> Campaign
        raise NotImplementedError
