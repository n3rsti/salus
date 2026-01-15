from sqlalchemy import func
from sqlmodel import Session, select
from api.database import engine
from api.models.activity_models import Activity
from api.models.program_day_activities_link import ProgramDayActivityLink
from api.models.program_models import Program, ProgramDay
from faker import Faker
import random

fake = Faker()


def populate_activities(new_activities_count: int = 100, new_programs_count: int = 50):
    session = Session(engine)

    for i in range(new_activities_count):
        activity = Activity(
            name=fake.sentence(nb_words=3),
            duration_minutes=fake.random_int(min=10, max=120),
            description=fake.paragraph(nb_sentences=3),
            difficulty=fake.random_int(min=1, max=3),
            owner_id=1,
            image_url=f"{fake.random_int(min=1, max=10)}.jpg",
        )
        session.add(activity)

    session.commit()

    activity_count = session.scalar(select(func.count()).select_from(Activity))
    if activity_count is None or activity_count == 0:
        return

    for i in range(new_programs_count):
        program = Program(
            name=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=4),
            duration_days=fake.random_int(min=7, max=30),
            language="en",
            image_url=f"{fake.random_int(min=1, max=10)}.jpg",
            owner_id=1,
        )
        session.add(program)
        session.flush()

        for j in range(program.duration_days):
            day = ProgramDay(
                description=fake.paragraph(nb_sentences=2),
                day_number=j + 1,
                program_id=program.id,
            )
            session.add(day)
            session.flush()

            num_activities = fake.random_int(min=1, max=5)

            selected_activity_ids = random.sample(
                range(1, activity_count + 1),
                min(num_activities, activity_count),
            )

            for activity_id in selected_activity_ids:
                link = ProgramDayActivityLink(
                    program_day_id=day.id,
                    activity_id=activity_id,
                )
                session.add(link)

    session.commit()
    session.close()


if __name__ == "__main__":
    populate_activities()
