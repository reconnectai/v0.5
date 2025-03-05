from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Reconnect.ai API", version="0.5")

# Static API key (v0.5 hack—move to PG/env later)
VALID_API_KEY = "reconnect-secret-2025"

# Mock DBs (PG later)
personae_db = {}
members_db = {}
artifacts_db = {}

# Persona Models
class PersonaCreate(BaseModel):
    name: str
    artifact_text: str  # Temp—v0.5 text-only

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    artifact_text: Optional[str] = None

# Member Models
class MemberCreate(BaseModel):
    email: str
    role: str
    subscription_status: str

class MemberUpdate(BaseModel):
    role: Optional[str] = None
    subscription_status: Optional[str] = None

# Artifact Models
class ArtifactCreate(BaseModel):
    persona_id: int
    content: str  # v0.5: text-only (ASCII, Word, PDF extracts)

class ArtifactUpdate(BaseModel):
    content: Optional[str] = None

# API Key Check
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Persona CRUD
@app.post("/persona/create")
async def create_persona(persona: PersonaCreate, member_id: int = Header(...), api_key: str = Header(...)):
    verify_api_key(api_key)
    persona_id = len(personae_db) + 1
    personae_db[persona_id] = {"member_id": member_id, **persona.dict()}
    # Auto-create first Artifact
    artifact_id = len(artifacts_db) + 1
    artifacts_db[artifact_id] = {"persona_id": persona_id, "content": persona.artifact_text}
    return {"persona_id": persona_id, "artifact_id": artifact_id}

@app.get("/persona/{persona_id}")
async def read_persona(persona_id: int, api_key: str = Header(...)):
    verify_api_key(api_key)
    if persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    return personae_db[persona_id]

@app.put("/persona/{persona_id}/update")
async def update_persona(persona_id: int, update: PersonaUpdate, api_key: str = Header(...)):
    verify_api_key(api_key)
    if persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    personae_db[persona_id].update({k: v for k, v in update.dict().items() if v is not None})
    return {"message": f"Persona {persona_id} updated"}

@app.delete("/persona/{persona_id}/delete")
async def delete_persona(persona_id: int, api_key: str = Header(...)):
    verify_api_key(api_key)
    if persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    # Cascade delete artifacts (v0.5 hack—PG will handle FKs)
    for aid, artifact in list(artifacts_db.items()):
        if artifact["persona_id"] == persona_id:
            del artifacts_db[aid]
    del personae_db[persona_id]
    return {"message": f"Persona {persona_id} deleted"}

# Member CRUD
@app.post("/users/create")
async def create_member(member: MemberCreate, member_id: int = Header(...), api_key: str = Header(...)):
    verify_api_key(api_key)
    if member_id in members_db:
        raise HTTPException(status_code=400, detail="Member already exists")
    members_db[member_id] = member.dict()
    return {"message": f"Member {member_id} created"}

@app.get("/users/{member_id}")
async def read_member(member_id: int, api_key: str = Header(...)):
    verify_api_key(api_key)
    if member_id not in members_db:
        raise HTTPException(status_code=404, detail="Member not found")
    return members_db[member_id]

@app.put("/users/{member_id}/update")
async def update_member(member_id: int, update: MemberUpdate, api_key: str = Header(...)):
    verify_api_key(api_key)
    if member_id not in members_db:
        raise HTTPException(status_code=404, detail="Member not found")
    members_db[member_id].update({k: v for k, v in update.dict().items() if v is not None})
    return {"message": f"Member {member_id} updated"}

@app.delete("/users/{member_id}/delete")
async def delete_member(member_id: int, api_key: str = Header(...)):
    verify_api_key(api_key)
    if member_id not in members_db:
        raise HTTPException(status_code=404, detail="Member not found")
    del members_db[member_id]
    return {"message": f"Member {member_id} deleted"}

# Artifact CRUD
@app.post("/artifact/create")
async def create_artifact(artifact: ArtifactCreate, member_id: int = Header(...), api_key: str = Header(...)):
    verify_api_key(api_key)
    if artifact.persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    if personae_db[artifact.persona_id]["member_id"] != member_id:
        raise HTTPException(status_code=403, detail="Unauthorized for this Persona")
    artifact_id = len(artifacts_db) + 1
    artifacts_db[artifact_id] = artifact.dict()
    return {"artifact_id": artifact_id}

@app.get("/artifact/{artifact_id}")
async def read_artifact(artifact_id: int, member_id: int = Header(...), api_key: str = Header(...)):
    verify_api_key(api_key)
    if artifact_id not in artifacts_db:
        raise HTTPException(status_code=404, detail="Artifact not found")
    artifact = artifacts_db[artifact_id]
    persona = personae_db[artifact["persona_id"]]
    if persona["member_id"] != member_id:
        raise HTTPException(status_code=403, detail="Unauthorized for this Artifact")
    return artifact

@app.put("/artifact/{artifact_id}/update")
async def update_artifact(artifact_id: int, update: ArtifactUpdate, member_id: int = Header(...), api_key: str = Header(...)):
    verify_api_key(api_key)
    if artifact_id not in artifacts_db:
        raise HTTPException(status_code=404, detail="Artifact not found")
    artifact = artifacts_db[artifact_id]
    if personae_db[artifact["persona_id"]]["member_id"] != member_id:
        raise HTTPException(status_code=403, detail="Unauthorized for this Artifact")
    artifacts_db[artifact_id].update({k: v for k, v in update.dict().items() if v is not None})
    return {"message": f"Artifact {artifact_id} updated"}

@app.delete("/artifact/{artifact_id}/delete")
async def delete_artifact(artifact_id: int, member_id: int = Header(...), api_key: str = Header(...)):
    verify_api_key(api_key)
    if artifact_id not in artifacts_db:
        raise HTTPException(status_code=404, detail="Artifact not found")
    artifact = artifacts_db[artifact_id]
    if personae_db[artifact["persona_id"]]["member_id"] != member_id:
        raise HTTPException(status_code=403, detail="Unauthorized for this Artifact")
    del artifacts_db[artifact_id]
    return {"message": f"Artifact {artifact_id} deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)