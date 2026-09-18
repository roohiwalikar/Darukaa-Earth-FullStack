from datetime import datetime,timedelta,timezone
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from jose import jwt
SECRET="change-me-in-production"; ALGO="HS256"
app=FastAPI(title="Darukaa.Earth API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
USERS={"admin@darukaa.earth":{"password":"password"}}
PROJECTS=[]; SITES=[]
class Login(BaseModel): email:str; password:str
class ProjectIn(BaseModel): name:str; description:str=""
class SiteIn(BaseModel): project_id:int; name:str; area_ha:float=Field(gt=0); geometry:dict
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/auth/login")
def login(x:Login):
    if x.email not in USERS or USERS[x.email]["password"]!=x.password: raise HTTPException(401,"Invalid credentials")
    token=jwt.encode({"sub":x.email,"exp":datetime.now(timezone.utc)+timedelta(hours=8)},SECRET,algorithm=ALGO)
    return {"access_token":token,"token_type":"bearer"}
@app.get("/projects")
def get_projects(): return PROJECTS
@app.post("/projects")
def create_project(x:ProjectIn):
    p={"id":len(PROJECTS)+1,"name":x.name,"description":x.description,"created_at":datetime.now(timezone.utc).isoformat()}; PROJECTS.append(p); return p
@app.get("/sites")
def get_sites(): return SITES
@app.post("/sites")
def create_site(x:SiteIn):
    s={"id":len(SITES)+1,**x.model_dump(),"created_at":datetime.now(timezone.utc).isoformat()}; SITES.append(s); return s
@app.get("/sites/{site_id}/analytics")
def analytics(site_id:int):
    if not any(s["id"]==site_id for s in SITES): raise HTTPException(404,"Site not found")
    return {"site_id":site_id,"periods":["Jan","Feb","Mar","Apr","May","Jun"],"carbon":[54,59,63,69,76,82],"biodiversity":[48,53,57,61,68,74]}
