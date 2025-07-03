#BASE_URL = "http://localhost:3001/api"  # ya da "https://pokeapi.co/api/v2"

import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:3001/api")