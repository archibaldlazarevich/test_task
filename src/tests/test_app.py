import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_task(ac: AsyncClient, setup_database):
    response = await ac.post(
        "/task/create",
        json={
            "task_name": "test task",
            "task_type": "test",
            "time_add": "2025-08-20T12:00:00",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["task_name"] == "test task"
    assert data["task_type"] == "test"


@pytest.mark.anyio
async def test_create_task_wrong(ac: AsyncClient, setup_database):
    response = await ac.post(
        "/task/create",
        json={
            "task_nam": "test task",
            "task_type": "test",
            "time_add": "2025-08-20T12:00:00",
        },
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_tasks(ac: AsyncClient, setup_database):
    response = await ac.get("/task")
    assert response.status_code == 200
    data = response.json()
    assert data[2]["task_name"] == "test task2"


@pytest.mark.anyio
async def test_get_task_by_id(ac: AsyncClient, setup_database):
    response = await ac.get("/task/3")
    if response.status_code == 200:
        data = response.json()
        assert "task_name" in data
        assert "task_type" in data
    else:
        assert response.status_code == 404


@pytest.mark.anyio
async def test_update_task(ac: AsyncClient, setup_database):
    response = await ac.patch(
        "/task/3",
        json={
            "id": 3,
            "task_name": "updated task",
            "task_type": "updated",
            "time_add": "2025-08-20T12:00:00",
        },
    )
    if response.status_code == 200:
        data = response.json()
        assert data["task_name"] == "updated task"
    else:
        assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_task(ac: AsyncClient, setup_database):
    response = await ac.delete("/task/3")
    if response.status_code == 200:
        data = response.json()
        assert "task_name" in data
    else:
        assert response.status_code == 404
