from datetime import datetime, timedelta, date
from typing import List, Tuple
from calendar import monthrange
from collections import deque
from fastapi.exceptions import HTTPException


class Worker:
    def __init__(self, fio: str = "") -> None:
        self.work_hour = 0
        self.fio = fio

class ShiftPlanner:

    __weekdays = {0: "Понедельник",
                  1: "Вторник",
                  2: "Среда",
                  3: "Четверг",
                  4: "Пятница",
                  5: "Суббота",
                  6: "Воскресенье"}

    def __init__(self, 
                 max_work_month: int, 
                 shift_time: int, 
                 shift_start: int, 
                 shift_end: int,
                 weekdays_weight: Tuple[int],
                 workers: List[Worker],
                 shifts_starts: Tuple[int]) -> None:
        self.max_work_month = max_work_month
        self.shift_time = shift_time
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.weekdays_weight = weekdays_weight
        self.workers = workers
        self.gen_workers = self.choice_worker()
        self.shifts_starts = shifts_starts

    def choice_worker(self):
        #Алгоритм выбора работников
        count = 0
        flag_stack = deque()
        while True:
            if count >= len(self.workers):
                count = 0
            worker: Worker = self.workers[count]
            
            #Проверка на превышения количества рабочих часов
            if worker.work_hour >= self.max_work_month:
                flag_stack.append(worker)
                #Если превышение количества рабочих часов у всех работников
                if flag_stack[0]==worker:
                    raise HTTPException(status_code=400, detail="У всех работников переработка. Назначьте больше работников или снизьте нагрузку")
                continue

            worker.work_hour += self.shift_time
            yield worker
            count += 1
            flag_stack.clear()

    def choice_start_work(self):
        #Алгоритм выбора начала смены для работника
        count = 0
        while True:
            if count >= len(self.shifts_starts):
                count = 0
            yield self.shifts_starts[count]
            count += 1

    def calculate_calendar(self, date: datetime):
        num_days = monthrange(date.year, date.month)[1] # Количество дней
        # print([i for i in range(num_days)])
        # for
        calendar = {}
        for i in range(1, num_days+1):
            calendar_date = datetime(year=date.year,
                                    month=date.month,
                                    day=i)
            calendar[i] = {"weekday": self.__weekdays[calendar_date.weekday()],
                           "workers": self.calculate_day(calendar_date)}

        return calendar
    
    def calculate_day(self, calendar_date: datetime):
        worker_list = deque()
        gen_start_hour = self.choice_start_work()
        for i in range(0, self.weekdays_weight[calendar_date.weekday()]):
            start_hour = next(gen_start_hour)

            date_start = datetime(year=calendar_date.year,
                                  month=calendar_date.month,
                                  day=calendar_date.day,
                                  hour=start_hour)
            data_end = datetime(year=calendar_date.year,
                                  month=calendar_date.month,
                                  day=calendar_date.day,
                                  hour=start_hour) + timedelta(hours=self.shift_time)
            
            worker_list.append({"name": next(self.gen_workers).fio,
                                "date_start": date_start.strftime(
                                                           "%Y-%m-%d %H:%M:%S"
                                                       ),
                                "date_end": data_end.strftime(
                                                           "%Y-%m-%d %H:%M:%S"
                                                       )
                                })
        return list(worker_list)
