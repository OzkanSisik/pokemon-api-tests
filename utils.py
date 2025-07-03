import time
import requests
import os


def wait_for_service(url, timeout=30, interval=2):
    """
    Wait for a service to become available at the given URL.
    timeout: maximum time to wait in seconds
    interval: time between retries in seconds
    """
    start = time.time()
    
    # Add health endpoint if not present
    if not url.endswith('/health'):
        health_url = f"{url}/health" if url.endswith('/') else f"{url}/health"
    else:
        health_url = url
    
    print(f"Waiting for service at {health_url}...")
    
    while True:
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"Service at {health_url} is ready!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Service not ready yet: {e}")
        
        if time.time() - start > timeout:
            raise TimeoutError(f"Service at {url} not available after {timeout} seconds")
        
        time.sleep(interval)


def get_base_url():
    """
    Get the base URL for the API, with fallback to localhost for local development
    """
    return os.getenv('BASE_URL', 'http://localhost:3001/api')
