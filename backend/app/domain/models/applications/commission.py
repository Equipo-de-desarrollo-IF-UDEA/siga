from datetime import datetime
from typing import Any

from odmantic import Model

class Commission(Model):
    country: str
    state: str | None
    city: str | None
    start_date: datetime
    end_date: datetime
    lenguage: str | None
    justification: str
    documents: list[Any] | None
    resolution: str | None
    cumplido: str | None
