from app import db, Meter, MeterData, app
from datetime import datetime, timedelta
import random


def get_random_datetime(start, delta):
    random_seconds = random.randint(0, int(delta.total_seconds()))
    random_datetime = start + timedelta(seconds=random_seconds)
    return random_datetime


def populate_db() -> None:
    try:
        # Add a meter
        if not Meter.query.first():
            for index in range(10):
                meter: Meter = Meter(
                                label="Temp Label",
                                )
                db.session.add(meter)
                db.session.commit()
                meter.label = f"Electric Meter: {meter.id}"
                db.session.commit()
                # Add meter data
                for data in range(10):
                    meter_data: MeterData = MeterData(
                                        meter_id=meter.id,
                                        timestamp=get_random_datetime(
                                            datetime.now(),
                                            timedelta(days=10
                                                      )
                                            ),
                                        value=index*100000 + data*100 + 123.45
                                        )
                    db.session.add(meter_data)
            db.session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback the session in case of error


if __name__ == "__main__":
    with app.app_context():
        populate_db()
