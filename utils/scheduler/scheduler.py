from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config import config


job_store = SQLAlchemyJobStore(url=config.connection_string_sync)
scheduler = AsyncIOScheduler()
scheduler.add_jobstore(job_store)



