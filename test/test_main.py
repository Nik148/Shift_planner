from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_generate_question(ac: AsyncClient):
    response = await ac.post("/get_calendar", json={
        "year": 2023,
        "month": 10,
        "max_work_month": 144,
        "shift_time": 12,
        "shift_start": 8,
        "shift_end": 22,
        "weekdays_weight": [
            3,
            2,
            2,
            2,
            2,
            2,
            1
        ],
        "workers_count": 10,
        "shifts_starts": [
            8, 10
        ]
    })
    
    assert response.status_code == 200
    assert len(response.json()) == 31