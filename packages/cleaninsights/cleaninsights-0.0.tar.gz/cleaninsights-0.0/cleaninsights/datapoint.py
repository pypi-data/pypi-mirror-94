from datetime import datetime
from typing import Optional


class DataPoint:
    campaign_id: str
    times: int
    first: datetime
    last: datetime

    def __init__(self, campaign_id: str, times: Optional[int],
                 first: Optional[datetime], last: Optional[datetime]):
        self.campaign_id = campaign_id
        self.times = 1 if times is None else times
        self.first = datetime.utcnow() if first is None else first
        self.last = datetime.utcnow() if last is None else last
