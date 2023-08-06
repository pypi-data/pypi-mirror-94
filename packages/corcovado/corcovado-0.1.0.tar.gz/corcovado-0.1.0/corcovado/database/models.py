import enum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Enum

from corcovado.database.settings import Base


class Type(enum.Enum):
    strenght = "strenght"
    power = "power"
    power_endurance = "power endurance"


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    type = Column(Enum(Type))
    sub_type = Column(String)
    work_time = Column(Integer, default=0, nullable=False)
    rest_time = Column(Integer, default=0, nullable=False)
    sets = Column(Integer, default=0, nullable=False)
    reps = Column(Integer, default=0, nullable=False)
    session_id = Column(Integer, ForeignKey("session.id"))
    session = relationship("Session")

    def __repr__(self):
        return f"<Exercise {id}>"


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    type = Column(Enum(Type))
    exercises = relationship(Exercise, backref="sessions")
    week_id = Column(Integer, ForeignKey("week.id"))
    week = relationship("Week")

    def __repr__(self):
        return f"<Session {id}>"


class Week(Base):
    __tablename__ = "week"

    id = Column(Integer, primary_key=True)
    day = Column(String)
    type = Column(Enum(Type))
    monday = relationship(Session)
    tuesday = relationship(Session)
    wednesday = relationship(Session)
    thursday = relationship(Session)
    friday = relationship(Session)
    saturday = relationship(Session)
    sunday = relationship(Session)
    planning_id = Column(Integer, ForeignKey("planning.id"))
    planning = relationship("Planning")

    def __repr__(self):
        return f"<Week {id}>"


class Planning(Base):
    __tablename__ = "planning"

    id = Column(Integer, primary_key=True)
    weeks = relationship(Week, backref="plannings")

    def __repr__(self):
        return f"<Planning {str(self.id)}>"
