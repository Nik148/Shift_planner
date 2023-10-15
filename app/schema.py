from pydantic import BaseModel, Field
from typing import List


class GetCalendarRequest(BaseModel):
    year: int
    month: int
    max_work_month: int
    shift_time: int
    shift_start: int
    shift_end: int
    weekdays_weight: List[int] = Field(min_length=7, max_length=7)
    workers_count: int
    shifts_starts: List[int] 