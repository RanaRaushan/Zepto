from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db import models
from db.database import SessionLocal, engine
from db.sql_service import update_seat_booking, add_coach_type, remove_coach_type, edit_coach_type


def start_app():

    ADD = "add"
    REMOVE = "remove"
    EDIT = "edit"

    @app.get("/")
    def home_page(request: Request):
        return templates.TemplateResponse('home.html', context={'request': request})

    @app.get("/user")
    def user_page(request: Request, db: Session = Depends(get_db)):
        records = db.query(models.Seat.seatNo, models.Seat.coachType).all()
        sorted_records = sorted(records, key=lambda y: (y[1], y[0]))
        return templates.TemplateResponse('home_user.html', context={'request': request, 'result': sorted_records})

    @app.post("/user")
    async def user_page_post(request: Request, data: list = Form(...), db: Session = Depends(get_db)):
        success_msg = "Successfully Booked"
        records = db.query(models.Seat.seatNo, models.Seat.coachType).all()
        sorted_records = sorted(records, key=lambda y: (y[1], y[0]))
        try:
            msg = update_seat_booking(db, data)
            if msg:
                success_msg = msg
        except Exception as e:
            print('Caught this error: ' + repr(e))
            success_msg = "Something Went Wrong! Try Again!"
        finally:
            return templates.TemplateResponse('home_user.html', context={'request': request, 'result': sorted_records,
                                                                         'success_msg': success_msg})

    @app.get("/admin_user")
    def admin_page(request: Request):
        return templates.TemplateResponse('home_adminUser.html', context={'request': request})

    @app.get("/update")
    def edit_page(request: Request, db: Session = Depends(get_db)):
        types_of_coach = db.query(models.Seat.coachType).distinct()
        return templates.TemplateResponse('add_data.html', context={'request': request, "coach": types_of_coach})

    @app.post("/update")
    async def edit_page_post(request: Request, db: Session = Depends(get_db)):
        form_data = await request.form()
        form_type = list(form_data.keys())[0]
        add_message = ""
        remove_message = ""
        edit_message = ""
        types_of_coach = db.query(models.Seat.coachType).distinct()
        if ADD in form_type:
            ct_add = (form_data.get("coach_type_add")).strip()
            no_of_seat = form_data.get("max_no_seat_add")
            add_message = "Please enter input!"
            if ct_add in [x[0] for x in types_of_coach]:
                add_message = "The coach type you have enter already exist!"
            elif ct_add and no_of_seat:
                add_coach_type(db, ct_add, int(no_of_seat))
                add_message = "Successfully added new coach type: {}, with {} no. of seat.".format(ct_add, no_of_seat)

        elif REMOVE in form_type:
            ct_remove = form_data.get("coach_type_remove")
            remove_message = "Please enter input!"
            if ct_remove:
                remove_coach_type(db, ct_remove)
                remove_message = "Successfully removed coach type: {}".format(ct_remove)
        elif EDIT in form_type:
            old_ct = (form_data.get("old_coach_type_edit")).strip()
            new_ct = (form_data.get("new_coach_type_edit")).strip()
            no_of_seat = form_data.get("new_no_of_seat_edit")
            edit_message = "Please enter input!"
            if new_ct in [x[0] for x in types_of_coach]:
                edit_message = "The new coach type you have enter already exist!"
            elif old_ct and new_ct and no_of_seat:
                edit_coach_type(db, new_ct, old_ct, int(no_of_seat))
                edit_message = "Successfully update coach type from {} to {}".format(old_ct, new_ct)
        types_of_coach = db.query(models.Seat.coachType).distinct()
        return templates.TemplateResponse('add_data.html', context={'request': request, "coach": types_of_coach,
                                                                    "add_message": add_message, "remove_message":
                                                                        remove_message, "edit_message": edit_message})

    @app.get("/availableSeat")
    def available_seat(request: Request, db: Session = Depends(get_db)):
        result = db.query(models.Seat.seatNo, models.Seat.coachType).filter_by(isBooked=False).all()
        result = sorted(result, key=lambda y: (y[1], y[0]))
        return templates.TemplateResponse('availableSeat.html', context={'request': request, 'result': result,
                                                                         'param': "Available"})

    @app.get("/allSeat")
    def all_seat(request: Request, db: Session = Depends(get_db)):
        list_result = db.query(models.Seat).all()
        list_result = sorted(list_result, key=lambda y: y.seatId)
        return templates.TemplateResponse('allSeatDetails.html', context={'request': request, 'result': list_result,
                                                                          'param': "All"})


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates/")
start_app()
