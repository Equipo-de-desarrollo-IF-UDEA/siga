from app.domain.models import Application, User
from app.domain.errors.application import *
from app.domain.schemas import ApplicationUpdate, ApplicationCreate
from .base import Base

# Here we handle Applications policies


class ApplicationPolicy(Base[Application, ApplicationCreate, ApplicationUpdate]):
    # who can see an Application of another user
    def get(self, who: User, to: Application) -> None:
        if not (who.rol.scope < 9) and not (who.id == to.user.id):
            raise application_401
        if not (who.rol.scope <= to.user.rol.scope):
            raise application_401
        if who.rol.scope == 7 or who.rol.scope == 6:
            if not (to.user.department_id == who.department_id):
                raise application_401
        if who.rol.scope == 5:
            if not (to.user.department.school_id == who.department.school_id):
                raise application_401
        if not to:
            raise application_404
        return None

    # Who can create a application of a subtype
    def create(self, who: User, to: ApplicationCreate,
               remunerated_permissions: int = 0) -> None:
        application_sub_type = to.application_sub_type_id
        if (application_sub_type in [1, 2, 3, 4, 5, 6, 7]
                and not (who.rol.scope == 11 or who.rol.scope == 9)):  # Permiso
            raise application_401
        if (application_sub_type in [8, 9]
                and not (who.rol.scope == 11 or who.rol.scope == 9)):  # Comisión
            raise application_401
        if (application_sub_type == 10 and not (who.rol.scope == 7)):  # Dedicación
            raise application_401
        return None
