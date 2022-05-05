from sqlalchemy.orm import Session
from datetime import date
from . import models
import string
import random


def add_user(db: Session, name, user_type):
    user_model = models.UserData(name=name, userType=user_type)
    db.add(user_model)
    db.commit()
    return user_model.userId


def update_train_booking(db: Session, booking_model_list):
    name = "anonymous_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    user_type = "customer"
    train_booking_model_list = []
    user_id = add_user(db, name, user_type)
    current_date = date.today().isoformat()
    for booking_model in booking_model_list:
        train_booking_model = models.TrainBooking(customer=user_id, seat=booking_model.seat, dates=current_date,
                                                  booking=booking_model.booking_id)
        train_booking_model_list.append(train_booking_model)
    db.add_all(train_booking_model_list)
    db.commit()


def update_booking(db: Session, seat_model_list):

    booking_model_list = []
    for seatModel in seat_model_list:
        booking_model = models.Booking(seat=seatModel.seatId)
        booking_model_list.append(booking_model)
    db.add_all(booking_model_list)
    db.commit()
    update_train_booking(db, booking_model_list)


def update_seat_booking(db: Session, list_of_seat):
    list_seat_model = []
    exception_msg = None
    for seat in list_of_seat:
        seat_no, coach = seat.split("-")
        seat_model = db.query(models.Seat).filter_by(seatNo=seat_no, coachType=coach, isBooked=False).first()
        if seat_model:
            seat_model.isBooked = True
            list_seat_model.append(seat_model)
    if len(list_seat_model) == len(list_of_seat):
        db.commit()
        update_booking(db, list_seat_model)
        pass
    else:
        exception_msg = "Selected Seats are already booked"
    return exception_msg


def add_coach_type(db: Session, new_coach_type, max_seat_no):
    list_seat_model = []
    for seatNumber in range(1, max_seat_no + 1):
        seat_model = models.Seat(seatNo=seatNumber, coachType=new_coach_type, isBooked=False)
        list_seat_model.append(seat_model)
    db.add_all(list_seat_model)
    db.commit()


def remove_coach_type(db: Session, coach_type):
    db.query(models.Seat).filter_by(coachType=coach_type).delete()
    db.commit()


def edit_coach_type(db: Session, new_coach_type, old_coach_type, update_seat_no):
    max_seat_no = db.query(models.Seat).filter_by(coachType=old_coach_type).update({"coachType": new_coach_type})
    if max_seat_no <= update_seat_no:
        list_seat_model = []
        for seatNumber in range(max_seat_no + 1, update_seat_no + 1):
            seat_model = models.Seat(seatNo=seatNumber, coachType=new_coach_type, isBooked=False)
            list_seat_model.append(seat_model)
        db.add_all(list_seat_model)
    else:
        db.query(models.Seat).filter(models.Seat.seatNo > update_seat_no).delete()

    db.commit()
