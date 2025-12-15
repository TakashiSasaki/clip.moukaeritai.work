
import json

from app.main import app
from fastapi.openapi.utils import get_openapi

def generate_openapi():
    openapi_schema = get_openapi(
        title="Clip Moukaeritai API",
        version="1.0.0",
        description="API documentation for Clip Moukaeritai, an auth-less web clipboard.",
        routes=app.routes,
    )
    
    # Save as JSON
    with open("static/openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
        
    print("Generated static/openapi.json")

if __name__ == "__main__":
    generate_openapi()
