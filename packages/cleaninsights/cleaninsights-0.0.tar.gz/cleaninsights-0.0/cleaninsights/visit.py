from datetime import datetime
from typing import List
from typing import Optional

from cleaninsights.datapoint import DataPoint


class Visit(DataPoint):
    path: List[str]

    def __init__(self, path: List[str], campaign_id: str, times: Optional[int],
                 first: Optional[datetime], last: Optional[datetime]):
        super().__init__(campaign_id, times, first, last)
        self.path = path
