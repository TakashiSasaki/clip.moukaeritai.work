# clip.moukaeritai.work

Welcome to **clip.moukaeritai.work**, a seamless, authentication-free web clipboard service.

## Concept

Your identity is your **UUIDv4**. 
You generate a random UUIDv4, and that becomes your private workspace.
No login required. Security relies on the mathematical improbability of guessing your UUID.

## How to Use

### 1. Get a UUID
You need a Version 4 UUID.
On Linux/Mac: `uuidgen`
On Python: `import uuid; uuid.uuid4()`

### 2. Store Data (API)
Use any HTTP client.

**PUT (Store with Key):**
```bash
curl -X PUT https://clip.moukaeritai.work/<YOUR_UUID>/my-note -d "Hello World"
```

**POST (Store with Auto-Generated Key):**
```bash
curl -X POST https://clip.moukaeritai.work/<YOUR_UUID> -d "Random Content"
# Returns: {"key": "sha1_hash_of_content"}
```

### 3. Retrieve Data
**GET (Single Item):**
```bash
curl https://clip.moukaeritai.work/<YOUR_UUID>/my-note
```

**GET (List Keys):**
```bash
curl https://clip.moukaeritai.work/<YOUR_UUID>
# Returns: {"keys": ["my-note", ...]}
```

### 4. Delete Data
```bash
curl -X DELETE https://clip.moukaeritai.work/<YOUR_UUID>/my-note
```

## Constraints
- **Value Size**: Max 1MB per item.
- **Key Length**: Max 100 characters.
- **Content**: UTF-8 String.
