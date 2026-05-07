import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker pattern for scraper resilience.
    
    Per-source circuit breakers prevent cascade failures:
    - Facebook: 5 failure threshold
    - Alibaba: 3 failure threshold (more fragile)
    - Amazon: 5 failure threshold
    """
    
    def __init__(self, name: str, failure_threshold: int = 5, recovery_timeout: int = 300):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception(f"Circuit {self.name} is OPEN — source unavailable")
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def get_state(self) -> str:
        return self.state.value

import asyncio

# Global circuit breakers
fb_circuit = CircuitBreaker("facebook_ads", failure_threshold=5)
alibaba_circuit = CircuitBreaker("alibaba", failure_threshold=3)
amazon_circuit = CircuitBreaker("amazon_pa_api", failure_threshold=5)
google_trends_circuit = CircuitBreaker("google_trends", failure_threshold=5)
