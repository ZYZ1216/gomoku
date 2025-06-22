# from fastapi import HTTPException,APIRouter, Depends, UploadFile, File
# from sqlalchemy.orm import Session
# import shutil
# import uuid
# import os
#
# from ..database import get_db
# from ..models import User
# from ..auth import get_current_user
#
# router = APIRouter()
#
# AVATAR_DIR = "static/avatars"
#
# # @router.post("/upload-avatar")
# @router.post("/me")
# def upload_avatar(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     # 生成唯一文件名
#     file_ext = os.path.splitext(file.filename)[1]
#     if file_ext.lower() not in [".jpg", ".jpeg", ".png"]:
#         raise HTTPException(
#             status_code=400,
#             detail="仅支持 JPG/PNG 格式"
#         )
#     unique_name = f"{uuid.uuid4().hex}{file_ext}"
#     save_path = os.path.join(AVATAR_DIR, unique_name)
#
#     # 保存文件
#     with open(save_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#
#     # 更新数据库
#     avatar_url = f"/static/avatars/{unique_name}"
#     current_user.avatar_url = avatar_url
#     db.commit()
#
#     return {"avatar_url": avatar_url}
#
#
# @router.get("/me")
# def get_current_user_info(
#     current_user: User = Depends(get_current_user),
# ):
#     return {
#         "id": current_user.id,
#         "username": current_user.username,
#         "avatar_url": current_user.avatar_url,
#         "created_at": current_user.created_at,
#     }

from fastapi import HTTPException, APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import uuid
import os

from ..database import get_db
from ..models import User
from ..auth import get_current_user

router = APIRouter(tags=["用户相关"])

AVATAR_DIR = "static/avatars"

@router.post("/me")
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_ext = os.path.splitext(file.filename)[1]
    if file_ext.lower() not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="仅支持 JPG/PNG 格式")

    # 删除旧头像（如果有）
    if current_user.avatar_url:
        old_path = current_user.avatar_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    # 保存新头像
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    save_path = os.path.join(AVATAR_DIR, unique_name)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 更新数据库
    avatar_url = f"/static/avatars/{unique_name}"
    current_user.avatar_url = avatar_url
    db.commit()

    return {
        "code": 200,
        "msg": "头像上传成功",
        "data": {
            "avatar_url": avatar_url
        }
    }

@router.get("/me")
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    return {
        "code": 200,
        "msg": "获取用户信息成功",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "avatar_url": current_user.avatar_url
        }
    }
