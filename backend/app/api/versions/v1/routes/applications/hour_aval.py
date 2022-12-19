from fastapi import APIRouter, Depends, HTTPException
from odmantic import ObjectId
from odmantic.session import AIOSession
from sqlalchemy.orm import Session

from app.api.middlewares import mongo_db, db, jwt_bearer
from app.core.logging import get_logging
from app.services import crud
from app.domain.models import HourAval, User, Application
from app.domain.schemas import (ApplicationCreate,
                                HourAvalCreate,
                                HourAvalUpdate,
                                Msg,
                                HourAvalResponse,
                                ApplicationResponse,
                                )
from app.domain.errors import BaseErrors


router = APIRouter()

log = get_logging(__name__)


@router.post("/", response_model=HourAvalResponse)
async def create_hour_aval(
    hour_aval: HourAvalCreate,
    *,
    current_user: User = Depends(jwt_bearer.get_current_active_user),
    engine: AIOSession = Depends(mongo_db.get_mongo_db),
    db: Session = Depends(db.get_db)
) -> HourAvalResponse:
    """
    Endpoint to create a application type hour_aval

        params:
            - body: hour_avalCreate

        response:
            - hour_aval
    """
    try:
        hour_aval_created = await crud.hour_aval.create(db=engine,
                                                          obj_in=HourAval(**dict(hour_aval)))

        application = ApplicationCreate(
            mongo_id=str(hour_aval_created.id),
            application_sub_type_id=hour_aval.application_sub_type_id,
            user_id=current_user.id
        )
        application = crud.application.create(
            db=db, who=current_user, obj_in=application)
    except BaseErrors as e:
        await engine.remove(hour_aval, hour_aval.id == hour_aval_created.id)
        log.error('BaseErrors')
        raise HTTPException(e.code, e.detail)
    except ValueError as e:
        log.error('ValueError')
        await engine.remove(hour_aval, hour_aval.id == hour_aval_created.id)
        raise HTTPException(422, e)
    except Exception as e:
        log.error('Exception')
        log.error(e)
        await engine.remove(hour_aval, hour_aval.id == hour_aval_created.id)
        raise HTTPException(422, "Algo ocurrió mal")
    application = ApplicationResponse.from_orm(application)
    response = HourAvalResponse(
        **dict(application),
        hour_aval=hour_aval_created
    )
    return response


@router.get("/", response_model=list[HourAval])
async def get_hour_avals(*,
                          engine: AIOSession = Depends(mongo_db.get_mongo_db)) -> list[HourAval]:

    hour_avales = await engine.find(HourAval)
    return hour_avales


@router.get("/{id}", response_model=HourAvalResponse)
async def get_hour_aval(
    id: int,
    *,
    current_user: User = Depends(jwt_bearer.get_current_active_user),
    engine: AIOSession = Depends(mongo_db.get_mongo_db),
    db: Session = Depends(db.get_db)
) -> HourAvalResponse:
    """
    Endpoint to ger a hour_aval model from mongo

        path-params:
            -id: int, this is the id of the application, not of mongo

        response:
            -body: hour_aval
    """
    try:
        application = crud.application.get(db, current_user, id=id)
        mongo_id = ObjectId(application.mongo_id)
        if application:
            hour_aval = await crud.hour_aval.get(engine, id=mongo_id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    application_response = ApplicationResponse.from_orm(application)
    response = HourAvalResponse(
        **dict(application_response),
        hour_aval=hour_aval
    )
    return response


@router.put("/{id}", status_code=200)
async def update_hour_aval(
    id: int,
    hour_aval: HourAvalUpdate,
    *,
    current_user: User = Depends(jwt_bearer.get_current_active_user),
    engine: AIOSession = Depends(mongo_db.get_mongo_db),
    db: Session = Depends(db.get_db)
) -> HourAval:
    """
    Endpoint to update an application of type hour_aval

        params:
            -body: hour_avalUpdate

        path-params:
            -id: int, this is the id of the application and not the mongo_id

        response:
            -body: hour_aval
    """

    try:
        # GET In PostgreSQL
        application: Application = crud.application.get(
            db=db, id=id, who=current_user)

        if application:

            log.debug('obj_in que es', hour_aval)

            # In MongoDB
            mongo_id = ObjectId(application.mongo_id)

            current_hour_aval = await crud.hour_aval.get(engine, id=mongo_id)

            updated_hour_aval = await crud.hour_aval.update(engine, db_obj=current_hour_aval, obj_in=hour_aval)

            log.debug('updated_hour_aval', updated_hour_aval)

            # In PostgreSQL
            application_updated = crud.application.update(
                db=db, who=current_user, db_obj=application, obj_in=hour_aval)

            log.debug('application update', application_updated)

    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)

    return updated_hour_aval


@router.delete("/{id}", response_model=Msg)
async def delete_hour_aval(
    id: int,
    *,
    current_user: User = Depends(jwt_bearer.get_current_active_user),
    engine: AIOSession = Depends(mongo_db.get_mongo_db),
    db: Session = Depends(db.get_db)
) -> Msg:
    """
    Endpoint to delete an application of type hour_aval

        params:
            -id: int, this is the id of the application and not of mongo

        response:
            -msg: Msg
    """
    try:
        # First get the application from postgresql
        application = crud.application.get(db, current_user, id=id)
        # get id from the model sql
        mongo_id = ObjectId(application.mongo_id)
        # Delete object in postgresql
        delete = crud.application.delete(db, current_user, id=id)
        log.debug(delete)
        if delete:
            log.debug('Estamos en delete')
            # delete object on Mongo
            await crud.hour_aval.delete(engine, id=mongo_id)

    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return Msg(msg="Comisión eliminada correctamente")
