from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import models, schemas, auth, database
from app.routers import users
from fastapi.openapi.docs import get_swagger_ui_html

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Gomoku API",
    description="五子棋项目后端接口",
    version="0.1.0",
    openapi_tags=[
        {"name": "用户相关", "description": "用户信息、头像上传、获取用户详情等"},
    ]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(users.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_ui_parameters={"persistAuthorization": True}
    )

origins = ["*"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return auth.create_user(user, db)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth.authenticate_user(user.username, user.password, db)
    if not db_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = auth.create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
