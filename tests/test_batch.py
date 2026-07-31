import time

from requests import BatchSession


def test_batch_session_starts_empty():
    batch = BatchSession()

    assert batch.queue_size() == 0
    
def test_queue_request_increases_queue_size():
    batch = BatchSession()

    batch.queue_get("https://example.com")

    assert batch.queue_size() == 1
    
def test_multiple_requests_are_queued():
    batch = BatchSession()

    batch.queue_get("https://example.com")
    batch.queue_get("https://github.com")
    batch.queue_post("https://httpbin.org/post")

    assert batch.queue_size() == 3
    
def test_execute_clears_queue():
    batch = BatchSession()

    batch.queue_get("https://example.com")

    batch.execute()

    assert batch.queue_size() == 0
    
def test_execute_returns_successful_batch_result():
    batch = BatchSession()

    batch.queue_get("https://example.com")

    results = batch.execute()

    assert len(results) == 1

    assert results[0].success is True
    assert results[0].response is not None
    assert results[0].exception is None
    
def test_execute_returns_failed_batch_result():
    batch = BatchSession()

    batch.queue_get("https://this-domain-does-not-exist-123456.com")

    results = batch.execute()

    assert len(results) == 1

    assert results[0].success is False
    assert results[0].response is None
    assert results[0].exception is not None

def test_execute_preserves_request_order():
    batch = BatchSession()

    batch.queue_get("https://example.com")
    batch.queue_get("https://www.google.com")

    results = batch.execute()

    assert len(results) == 2

    assert results[0].response is not None
    assert results[1].response is not None

    assert results[0].response.url == "https://example.com/"
    assert results[1].response.url == "https://www.google.com/"
    