from fastapi import FastAPI
import httpx
import asyncio
import contextlib
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# engine = create_async_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Start process {os.getpid()}', flush=True)
    yield
    if async_db_obj.engine:
        print("Dispose async_db_obj", flush=True)
        await async_db_obj.async_close()
    if db_obj.engine:
        print(f"Dispose db_obj", flush=True)
        db_obj.close()

app = FastAPI(lifespan=lifespan)

# Airflow Webserver의 내부 컨테이너 네트워크 주소
AIRFLOW_API_URL = "http://airflow-webserver:8080/api/v1/dags"

@app.post("/trigger_dag/{dag_id}", tags=["Airflow"])
async def trigger_dag(dag_id: str):
    """
    특정 DAG을 실행하는 API

    - **dag_id**: 실행할 DAG의 ID
    """
    url = f"{AIRFLOW_API_URL}/{dag_id}/dagRuns"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={}, auth=("airflow", "airflow"))  # 기본 인증 추가
    return response.json()

