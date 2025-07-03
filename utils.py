import time
import requests

def wait_for_service(url, timeout=2, interval=1):
    """
    Verilen URL'e bağlanmayı dener.
    timeout saniye sonunda servis açılmazsa hata verir.
    interval saniye aralıklarla tekrar dener.
    """
    start = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass

        if time.time() - start > timeout:
            raise TimeoutError(f"Service at {url} not available after {timeout} seconds")
        time.sleep(interval)
