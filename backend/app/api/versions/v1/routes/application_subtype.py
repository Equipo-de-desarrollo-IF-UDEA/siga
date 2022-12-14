from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.api.middlewares import db, jwt_bearer
from app.domain import schemas
from app.domain.errors.base import BaseErrors
from app.services import crud

router = APIRouter()


@router.get("/{id}", status_code=200, response_model=schemas.ApplicationSubTypeInDB)
def get_application_sub_type(
    id: int,
    *,
    db: Session = Depends(db.get_db),
    current_user: schemas.UserInDB = Depends(
        jwt_bearer.get_current_active_user),
) -> Any:
    """
    Endpoint to read one Application Sub type.

        params: id:int
    """
    try:
        db_application_sub_type = crud.application_sub_type.get(
            db=db, id=id, who=current_user)
    except BaseErrors as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    return db_application_sub_type