from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from zepto_train_booking.db.database import SQLALCHEMY_DATABASE_URL


def one_time_execute():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    db = scoped_session(sessionmaker(bind=engine))
    existing_coach = {"A/C Sleeper": 60, "Non A/C Sleeper": 60, "Seater": 120}
    incr = 1000
    for coach, seat in existing_coach.items():
        for i in range(1, seat + 1):
            incr += 1
            insert_query = "INSERT into seat (\"seatNo\", \"isBooked\", \"coachType\") values({}, FALSE, '{}');" \
                .format(i, coach)
            db.execute(insert_query)

    db.commit()
    db.close()


one_time_execute()

