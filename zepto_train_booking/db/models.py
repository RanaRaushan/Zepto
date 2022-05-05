from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from .database import Base


class TrainBooking(Base):
    __tablename__ = "train_booking"

    tb_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer = Column(Integer, ForeignKey("user_data.userId"), index=True)
    seat = Column(Integer, ForeignKey("seat.seatId"))
    dates = Column(Date)
    booking = Column(Integer, ForeignKey("booking.booking_id"))

    TrainToSeat = relationship("Seat", backref=backref("train_booking", uselist=False))
    TrainToUser = relationship("UserData", backref=backref("train_booking", uselist=False))
    TrainToBooking = relationship("Booking", backref=backref("train_booking", uselist=False))


class Seat(Base):
    __tablename__ = "seat"

    seatId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    seatNo = Column(Integer)
    isBooked = Column(Boolean, default=False)
    coachType = Column(String)
    UniqueConstraint(seatNo, coachType)


class UserData(Base):
    __tablename__ = "user_data"

    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    userType = Column(String)


class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # booking_id = Column(Integer)
    seat = Column(Integer, ForeignKey("seat.seatId"))

    BookingToSeat = relationship("Seat", backref=backref("booking", uselist=False))

