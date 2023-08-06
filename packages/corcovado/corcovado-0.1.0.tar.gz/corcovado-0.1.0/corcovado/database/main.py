from corcovado.database.models import Exercise
from corcovado.database.models import Planning
from corcovado.database.models import Session
from corcovado.database.models import Type
from corcovado.database.models import Week
from corcovado.database.settings import Base
from corcovado.database.settings import db_session
from corcovado.database.settings import engine


def init_db(engine=engine):

    Base.metadata.create_all(bind=engine)
    Exercise.__table__.create(bind=engine, checkfirst=True)
    Session.__table__.create(bind=engine, checkfirst=True)
    Week.__table__.create(bind=engine, checkfirst=True)
    Planning.__table__.create(bind=engine, checkfirst=True)
    print("Initialized the db")


if __name__ == "__main__":
    init_db()
