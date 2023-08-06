from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from cleaninsights.event import Event
from cleaninsights.visit import Visit


class Store:
    events: List[Event]
    visits: List[Visit]

    def __init__(self, *args, **kwargs):
        data = self.load(*args, **kwargs)
        if data is None:
            raise RuntimeError("Storage doesn't exist or isn't readable.")
        if 'events' in data:
            self.events = [Event(**e) for e in data['events']]
        if 'visits' in data:
            self.visits = [Visit(**v) for v in data['visits']]

    def load(self, *args,
             **kwargs) -> Optional[List[Dict[str, Union[str, int, float]]]]:
        raise NotImplementedError

    def persist(self) -> None:
        raise NotImplementedError

    def send(self, data: str, server: str, timeout: int) -> bool:
        raise NotImplementedError
