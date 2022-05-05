from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from .models import TrainBooking, UserData, Seat, Booking

TrainBookingSchema = sqlalchemy_to_pydantic(TrainBooking)
UserDataSchema = sqlalchemy_to_pydantic(UserData)
SeatSchema = sqlalchemy_to_pydantic(Seat)
BookingSchema = sqlalchemy_to_pydantic(Booking)
