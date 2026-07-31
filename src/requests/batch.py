from .sessions import Session
from dataclasses import dataclass
from typing import Any

from . import _internal_utils as _t
from .models import Request

from concurrent.futures import ThreadPoolExecutor

@dataclass
class QueuedRequest:
    request: Request
    send_kwargs: dict[str, Any]

class BatchSession(Session):
    def __init__(self, workers: int = 4):
        super().__init__()
        self.workers = workers
        self._queue: list[QueuedRequest] = []
        
    def queue_request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> None:
        request = Request(
            method=method,
            url=url,
        )

        self._queue.append(
            QueuedRequest(
                request=request,
                send_kwargs=kwargs,
            )
        )
    
    def queue_size(self) -> int:
        return len(self._queue) 
    
    def _execute_request(self, item: QueuedRequest):
        
        response = super().request(
            method=item.request.method,
            url=item.request.url,
            params=item.request.params,
            data=item.request.data,
            headers=item.request.headers,
            cookies=item.request.cookies,
            files=item.request.files,
            auth=item.request.auth,
            hooks=item.request.hooks,
            json=item.request.json,
            **item.send_kwargs,
        )
        
        return response
        
    
    def execute(self):

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            responses = list(
                executor.map(self._execute_request, self._queue)
            )
        
        self._queue.clear()
        
        return responses
            