from typing import Dict, List

from corcovado.database.models import Exercise
from corcovado.database.settings import Base


class Repository:
    def __init__(self, session, model) -> None:
        self._model: Base = model
        self._session = session

    def list(self) -> List[Base]:
        return self._session.query(self._model).all()

    def create(self, data: Dict):
        entry = self._model(**data)
        self._session.add(entry)
        self._session.commit()
        return entry

    def get(self, data: Dict):
        return self._session.query(self._model).filter_by(**data).one()

    def update(self, instance, data: Dict):
        self._session.query(self._model).filter(self._model.id==instance.id).update(data, synchronize_session=False)
        self._session.commit()

    def delete(self, instance):
        self._session.delete(instance)
        self._session.commit()
