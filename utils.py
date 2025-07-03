import os

def get_base_url():
    """
    Get the base URL for the API, with fallback to localhost for local development
    """
    return os.getenv('BASE_URL', 'http://localhost:3001/api')
