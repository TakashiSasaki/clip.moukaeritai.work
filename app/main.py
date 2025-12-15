from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import os

from app.config import MAX_VALUE_SIZE_BYTES, MAX_KEY_LENGTH
from app.utils import is_valid_uuid4
from app.database import init_db, put_item, get_item, delete_item, list_keys

app = FastAPI(title="Clip Moukaeritai")

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Allowed files for static serving via specific routes
STATIC_DIR = "static"

@app.get("/status")
def get_status():
    return {"status": "running"}

@app.get("/mcp")
def get_mcp():
    # Placeholder for MCP
    return {"status": "mcp_endpoint_ready", "details": "not_implemented_yet"}

@app.get("/index.html")
def get_index_html():
    path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="index.html not found")

@app.get("/index.md")
def get_index_md():
    path = os.path.join(STATIC_DIR, "index.md")
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="index.md not found")

@app.get("/test.html")
def get_test_html():
    path = os.path.join(STATIC_DIR, "test.html")
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="test.html not found")

@app.get("/")
def read_root():
    # Redirect or just serve index.html? spec doesn't mandate root behavior, 
    # but strictly says index.html is landing page.
    # Let's redirect to index.html for convenience.
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/index.html")

# --- Clipboard API ---

@app.get("/{uuid_str}")
def list_clipboard_keys(uuid_str: str):
    if not is_valid_uuid4(uuid_str):
        raise HTTPException(status_code=404, detail="Invalid UUID")
    
    keys = list_keys(uuid_str)
    return {"keys": keys}

@app.post("/{uuid_str}")
async def post_new_item(uuid_str: str, request: Request):
    if not is_valid_uuid4(uuid_str):
        raise HTTPException(status_code=404, detail="Invalid UUID")
    
    body = await request.body()
    if len(body) > MAX_VALUE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail={"error": "Payload too large", "max_bytes": MAX_VALUE_SIZE_BYTES})
        
    try:
        value = body.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail={"error": "Body must be valid UTF-8"})
    
    # Generate SHA1 key
    key = hashlib.sha1(body).hexdigest()
    
    # Check key length? SHA1 hexdigest is 40 chars. Usually fits in 100.
    if len(key) > MAX_KEY_LENGTH:
         # Should not happen for SHA1 (40 chars)
         raise HTTPException(status_code=500, detail={"error": "Generated key too long"})

    put_item(uuid_str, key, value)
    return {"key": key}

@app.get("/{uuid_str}/{key}")
def get_clipboard_item(uuid_str: str, key: str):
    if not is_valid_uuid4(uuid_str):
        raise HTTPException(status_code=404, detail="Invalid UUID")
    
    value = get_item(uuid_str, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Item not found")
        
    return Response(content=value, media_type="text/plain")

@app.put("/{uuid_str}/{key}")
async def put_clipboard_item(uuid_str: str, key: str, request: Request):
    if not is_valid_uuid4(uuid_str):
        raise HTTPException(status_code=404, detail="Invalid UUID")
    
    if len(key) > MAX_KEY_LENGTH:
        raise HTTPException(status_code=413, detail={"error": "Key too long", "max_chars": MAX_KEY_LENGTH})
        
    body = await request.body()
    if len(body) > MAX_VALUE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail={"error": "Payload too large", "max_bytes": MAX_VALUE_SIZE_BYTES})
        
    try:
        value = body.decode('utf-8')
    except UnicodeDecodeError:
         raise HTTPException(status_code=400, detail={"error": "Body must be valid UTF-8"})

    put_item(uuid_str, key, value)
    return {"status": "ok", "key": key}

@app.delete("/{uuid_str}/{key}")
def delete_clipboard_item(uuid_str: str, key: str):
    if not is_valid_uuid4(uuid_str):
        raise HTTPException(status_code=404, detail="Invalid UUID")
        
    # Check if exists? Or just delete (idempotent)
    # Spec doesn't require 404 on delete if not exists.
    delete_item(uuid_str, key)
    return {"status": "deleted", "key": key}
