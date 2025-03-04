from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Reconnect.ai API", version="0.5")

# Mock DBs (replace with Postgres/pgvector later)
personae_db = {}
members_db = {}

# Persona Models
class PersonaCreate(BaseModel):
    name: str
    artifact_text: str

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    artifact_text: Optional[str] = None

# Member Models
class MemberCreate(BaseModel):
    id: int  # WP user ID
    email: str
    role: str  # e.g., "subscriber", "premium"
    subscription_status: str  # e.g., "active", "inactive"

class MemberUpdate(BaseModel):
    role: Optional[str] = None
    subscription_status: Optional[str] = None

# Persona CRUD
@app.post("/persona/create")
async def create_persona(persona: PersonaCreate):
    persona_id = len(personae_db) + 1
    personae_db[persona_id] = persona.dict()
    return {"persona_id": persona_id}

@app.get("/persona/{persona_id}")
async def read_persona(persona_id: int):
    if persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    return personae_db[persona_id]

@app.put("/persona/{persona_id}/update")
async def update_persona(persona_id: int, update: PersonaUpdate):
    if persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    personae_db[persona_id].update({k: v for k, v in update.dict().items() if v is not None})
    return {"message": f"Persona {persona_id} updated"}

@app.delete("/persona/{persona_id}/delete")
async def delete_persona(persona_id: int):
    if persona_id not in personae_db:
        raise HTTPException(status_code=404, detail="Persona not found")
    del personae_db[persona_id]
    return {"message": f"Persona {persona_id} deleted"}

# Member CRUD
@app.post("/users/create")
async def create_member(member: MemberCreate):
    if member.id in members_db:
        raise HTTPException(status_code=400, detail="Member already exists")
    members_db[member.id] = member.dict()
    return {"message": f"Member {member.id} created"}

@app.get("/users/{member_id}")
async def read_member(member_id: int):
    if member_id not in members_db:
        raise HTTPException(status_code=404, detail="Member not found")
    return members_db[member_id]

@app.put("/users/{member_id}/update")
async def update_member(member_id: int, update: MemberUpdate):
    if member_id not in members_db:
        raise HTTPException(status_code=404, detail="Member not found")
    members_db[member_id].update({k: v for k, v in update.dict().items() if v is not None})
    return {"message": f"Member {member_id} updated"}

@app.delete("/users/{member_id}/delete")
async def delete_member(member_id: int):
    if member_id not in members_db:
        raise HTTPException(status_code=404, detail="Member not found")
    del members_db[member_id]
    return {"message": f"Member {member_id} deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)