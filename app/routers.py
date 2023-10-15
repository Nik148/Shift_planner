from fastapi import APIRouter
from datetime import datetime
from app.schema import GetCalendarRequest
from app.ShiftPlanner import ShiftPlanner, Worker
from app.doc import get_calendar_desription


router = APIRouter(prefix="", tags=["Shift Planner"])

@router.post("/get_calendar", description=get_calendar_desription)
def get_calendar(data: GetCalendarRequest):
    workers = [Worker(str(i)) for i in range(data.workers_count)]
    shiftPlanner = ShiftPlanner(workers=workers, **data.dict(exclude=("workers_count","year","month")))
    return shiftPlanner.calculate_calendar(datetime(year=data.year,
                                                    month=data.month,
                                                    day=1))
