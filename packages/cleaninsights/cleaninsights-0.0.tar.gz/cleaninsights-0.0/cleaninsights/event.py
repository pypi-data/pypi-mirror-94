from datetime import datetime
from typing import Optional
from typing import Union

from cleaninsights.datapoint import DataPoint


class Event(DataPoint):
    category: str
    action: Optional[str]
    name: Optional[str]
    value: Optional[Union[int, float]]

    def __init__(self, category: str, action: Optional[str],
                 name: Optional[str], value: Optional[Union[int, float]],
                 campaign_id: str, times: Optional[int],
                 first: Optional[datetime], last: Optional[datetime]):
        super().__init__(campaign_id, times, first, last)
        self.category = category
        self.action = action
        self.name = name
        self.value = value
