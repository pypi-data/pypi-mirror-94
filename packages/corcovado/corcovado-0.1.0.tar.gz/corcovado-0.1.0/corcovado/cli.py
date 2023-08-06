"""CLI for whattodo project."""
from typing import Optional

import typer

from rich.console import Console
from rich.table import Table
from sqlalchemy.sql.schema import Column

from corcovado.database.models import Exercise, Week
from corcovado.database.models import Planning
from corcovado.database.models import Session
from corcovado.database.models import Type
from corcovado.database.repository import Repository
from corcovado.database.settings import db_session

app = typer.Typer(help="GoClimb CLI manager.")
state = {"verbose": False}


@app.command("exercise:list")
def list_exercises():
    repository = Repository(model=Exercise, session=db_session)
    exercises = repository.list()
    build_exercise_list(exercises)


@app.command("planning")
def list_planning():
    repository = Repository(model=Planning, session=db_session)
    plannings = repository.list()
    build_planning(plannings)


def build_planning(plannings):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Week", style="dim", width=12)
    table.add_column("DAY", justify="center")
    table.add_column("MONDAY", justify="center")
    table.add_column("TUESDAY", justify="center")
    table.add_column("WEDNESDAY", justify="center")
    table.add_column("THURSDAY", justify="center")
    table.add_column("FRIDAY", justify="center")
    table.add_column("SATURDAY", justify="center")
    table.add_column("SUNDAY", justify="center")
    for planning in plannings:
        for index, week in enumerate(planning.weeks, start=1):
            table.add_row(
                f"WEEK {index}",
                f"{week.day}",
                f"{get_type_of(week.monday)}",
                f"{get_type_of(week.tuesday)}",
                f"{get_type_of(week.wednesday)}",
                f"{get_type_of(week.thursday)}",
                f"{get_type_of(week.friday)}",
                f"{get_type_of(week.saturday)}",
                f"{get_type_of(week.sunday)}",
            )
    console.print(table)


def get_type_of(week_day: Column) -> Optional[str]:
    return week_day[0].type.value if week_day else None


def build_exercise_list(exercises):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Exercise", style="dim", width=12)
    table.add_column("Reps")
    table.add_column("Sets")
    table.add_column("Rest")
    table.add_column("Notes")
    for exercise in exercises:
        table.add_row(
            f"{exercise.id}",
            f"{exercise.name}",
            f"{exercise.reps}",
            f"{exercise.sets}",
            f"{exercise.rest_time}",
            f"{exercise.description}",
        )
    console.print(table)


@app.command("exercise:add")
def add_exercise():
    """
    Creates a new Exercise.
    """
    typer.echo(f"Creating an [Exercise")
    repository = Repository(model=Exercise, session=db_session)
    name = typer.prompt("What's the Exercise name?")
    typer.echo(f"{name}")
    description = typer.prompt("What's the Exercise description?")
    typer.echo(f"{description}")
    type = typer.prompt("What's the Exercise type?")
    typer.echo(f"{type}")
    work_time = typer.prompt("What's the Exercise work time?")
    typer.echo(f"{work_time}")
    rest_time = typer.prompt("What's the Exercise rest time?")
    typer.echo(f"{rest_time}")
    sets = typer.prompt("What's the number of Sets?")
    typer.echo(f"{sets}")
    reps = typer.prompt("What's the number of Repetitions?")
    typer.echo(f"{reps}")
    repository.create(
        {
            "name": name,
            "description": description,
            "type": Type.strenght,
            "work_time": work_time,
            "rest_time": rest_time,
            "sets": sets,
            "reps": reps,
        }
    )


@app.command("session:add")
def add_session():
    """
    Creates a new Session.
    """
    typer.echo(f"Creating an [Session")
    repository = Repository(model=Session, session=db_session)
    name = typer.prompt("What's the Session name?")
    typer.echo(f"{name}")
    description = typer.prompt("What's the Session description?")
    typer.echo(f"{description}")
    type = typer.prompt("What's the Session type?")
    typer.echo(f"{type}")
    exercises = typer.prompt("What's the Session exercises?")
    typer.echo(f"{exercises}")
    exercises_ids = exercises.split(",")
    exercise_repo = Repository(model=Exercise, session=db_session)
    exercises_entries = [exercise_repo.get({"id": int(id)}) for id in exercises_ids]
    repository.create(
        {
            "name": name,
            "description": description,
            "type": Type.strenght,
            "exercises": exercises_entries,
        }
    )


@app.command("week:add")
def add_week():
    """
    Creates a new Week plan.
    """
    typer.echo(f"Creating a [Week]")
    repository = Repository(model=Week, session=db_session)
    day = typer.prompt("What's the Week first day?")
    typer.echo(f"{day}")
    type = typer.prompt("What's the Week type?")
    typer.echo(f"{type}")
    sessions = typer.prompt("What's the Week session IDs?")
    typer.echo(f"{sessions}")
    sessions_ids = sessions.split(",")
    session_repo = Repository(model=Session, session=db_session)
    sessions_entries = [session_repo.get({"id": int(id)}) for id in sessions_ids]
    repository.create(
        {
            "day": day,
            "type": Type.strenght,
            "sessions": sessions_entries,
        }
    )


@app.command("planning:add")
def add_planning():
    """
    Creates a new Planning.
    """
    typer.echo(f"Creating a [Planning]")
    repository = Repository(model=Planning, session=db_session)
    weeks = typer.prompt("What's the Planning week IDs?")
    typer.echo(f"{weeks}")
    weeks_ids = weeks.split(",")
    week_repo = Repository(model=Week, session=db_session)
    weeks_entries = [week_repo.get({"id": int(id)}) for id in weeks_ids]
    repository.create(
        {
            "weeks": weeks_entries,
        }
    )


# @app.command("session:start")
# def start_session():

#     typer.echo(f"Starting a [Session")
#     repository = Repository(model=Session, session=db_session)
#     session = repository.get({"id": 2})
#     for exercise in session.exercises:
#         for rep in range(exercise.reps):
#             typer.echo(f"Rep {rep + 1}/{exercise.reps}")
#             for set in range(exercise.sets):
#                 typer.echo(f"Set {set + 1}/{exercise.sets}")
#                 typer.echo(f"exercise {exercise.work_time}")
#                 data = {
#                     "timespec": str(exercise.work_time),
#                     "alt_format": False,
#                     "blink": False,
#                     "no_bell": False,
#                     "critical": 3,
#                     "font": "univers",
#                     "voice_prefix": None,
#                     "quit_after": None,
#                     "no_seconds": False,
#                     "text": None,
#                     "title": None,
#                     "no_window_title": False,
#                     "voice": None,
#                     "outfile": None,
#                     "exec_cmd": None,
#                     "no_figlet": False,
#                     "no_figlet_y_offset": -1,
#                     "no_text_magic": False,
#                     "time": False,
#                     "time_format": None,
#                 }
#                 curses.wrapper(countdown, **data)
#                 typer.echo(f"exercise {exercise.rest_time}")
#                 data = {
#                     "timespec": str(exercise.rest_time),
#                     "alt_format": False,
#                     "blink": False,
#                     "no_bell": False,
#                     "critical": 3,
#                     "font": "univers",
#                     "voice_prefix": None,
#                     "quit_after": None,
#                     "no_seconds": False,
#                     "text": None,
#                     "title": None,
#                     "no_window_title": False,
#                     "voice": None,
#                     "outfile": None,
#                     "exec_cmd": None,
#                     "no_figlet": False,
#                     "no_figlet_y_offset": -1,
#                     "no_text_magic": False,
#                     "time": False,
#                     "time_format": None,
#                 }
#                 curses.wrapper(countdown, **data)


@app.callback()
def main(verbose: bool = False):
    """
    Manage Climbing workouts in the awesome CLI app.
    """
    if verbose:
        typer.echo("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()
