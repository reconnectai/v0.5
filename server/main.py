from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from db import (create_member, read_member, update_member, delete_member,
                      create_persona, read_persona, update_persona, delete_persona,
                      create_artifact, read_artifact, update_artifact, delete_artifact)

app = FastAPI(title="Reconnect.ai API", version="0.5")

VALID_API_KEY = "reconnect-secret-2025"

# Models (same as before)
class PersonaCreate(BaseModel):
    name: str
    artifact_text: str

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    artifact_text: Optional[str] = None

class MemberCreate(BaseModel):
    email: str
    role: str
    subscription_status: str

class MemberUpdate(BaseModel):
    role: Optional[str] = None
    subscription_status: Optional[str] = None

class ArtifactCreate(BaseModel):
    persona_id: int
    content: str

class ArtifactUpdate(BaseModel):
    content: Optional[str] = None

# API Key Check
def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Persona CRUD
@app.post("/persona/create")
async def create_persona_endpoint(persona: PersonaCreate, member_id: int = Header(...), api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    try:
        persona_id = create_persona(persona.dict(), member_id)
        return {"persona_id": persona_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/persona/{persona_id}")
async def read_persona_endpoint(persona_id: int, api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    persona = read_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona

@app.put("/persona/{persona_id}/update")
async def update_persona_endpoint(persona_id: int, update: PersonaUpdate, api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    if not update_persona(persona_id, update.dict(exclude_unset=True)):
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": f"Persona {persona_id} updated"}

@app.delete("/persona/{persona_id}/delete")
async def delete_persona_endpoint(persona_id: int, api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    if not delete_persona(persona_id):
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": f"Persona {persona_id} deleted"}

# Member CRUD
@app.post("/users/create")
async def create_member_endpoint(member: MemberCreate, member_id: int = Header(...), api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    if not create_member(member.dict(), member_id):
        raise HTTPException(status_code=400, detail="Member already exists")
    return {"message": f"Member {member_id} created"}

@app.get("/users/{member_id}")
async def read_member_endpoint(member_id: int, api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    member = read_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.put("/users/{member_id}/update")
async def update_member_endpoint(member_id: int, update: MemberUpdate, api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    if not update_member(member_id, update.dict(exclude_unset=True)):
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": f"Member {member_id} updated"}

@app.delete("/users/{member_id}/delete")
async def delete_member_endpoint(member_id: int, api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    if not delete_member(member_id):
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": f"Member {member_id} deleted"}

# Artifact CRUD
@app.post("/artifact/create")
async def create_artifact_endpoint(artifact: ArtifactCreate, member_id: int = Header(...), api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    try:
        artifact_id = create_artifact(artifact.dict(), member_id)
        return {"artifact_id": artifact_id}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/artifact/{artifact_id}")
async def read_artifact_endpoint(artifact_id: int, member_id: int = Header(...), api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    artifact = read_artifact(artifact_id, member_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found or unauthorized")
    return artifact

@app.put("/artifact/{artifact_id}/update")
async def update_artifact_endpoint(artifact_id: int, update: ArtifactUpdate, member_id: int = Header(...), api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    try:
        if not update_artifact(artifact_id, update.dict(exclude_unset=True), member_id):
            raise HTTPException(status_code=404, detail="Artifact not found or unauthorized")
        return {"message": f"Artifact {artifact_id} updated"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.delete("/artifact/{artifact_id}/delete")
async def delete_artifact_endpoint(artifact_id: int, member_id: int = Header(...), api_key: str = Header(..., alias="x-api-key")):
    verify_api_key(api_key)
    try:
        if not delete_artifact(artifact_id, member_id):
            raise HTTPException(status_code=404, detail="Artifact not found or unauthorized")
        return {"message": f"Artifact {artifact_id} deleted"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)