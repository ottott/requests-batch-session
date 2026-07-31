from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from .models import Request, Response
from .sessions import Session


@dataclass
class QueuedRequest:
    request: Request
    send_kwargs: dict[str, Any]
    
@dataclass
class BatchResult:
    success: bool
    response: Response | None = None
    exception: Exception | None = None

class BatchSession(Session):
    def __init__(self, workers: int = 8) -> None:
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
    
    def queue_get(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("GET", url, **kwargs)
        
    def queue_post(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("POST", url, **kwargs)
        
    def queue_put(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("PUT", url, **kwargs)
    
    def queue_patch(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("PATCH", url, **kwargs)
        
    def queue_delete(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("DELETE", url, **kwargs)
        
    def queue_head(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("HEAD", url, **kwargs)
        
    def queue_options(
        self,
        url: str,
        **kwargs: Any,
    ) -> None:
        self.queue_request("OPTIONS", url, **kwargs)
    
    def queue_size(self) -> int:
        return len(self._queue) 
    
    
    def _execute_request(self, item: QueuedRequest) -> BatchResult:
        assert item.request.method is not None
        assert item.request.url is not None
        
        try:    
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
            
            return BatchResult(
                success=True,
                response=response
            )
            
        except Exception as e:
            return BatchResult(
                success=False,
                exception=e
            )
        
    
    def execute(self) -> list[BatchResult]:
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            responses = list(
                executor.map(self._execute_request, self._queue)
            )
        
        self._queue.clear()
        
        return responses
            