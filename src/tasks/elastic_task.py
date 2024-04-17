"""elsatic task"""
import asyncio

from elasticsearch import Elasticsearch

from src.db.session import clear_db_session
from src.services.elastic_search.controller import ElasticSearchController
from src.tasks.celery import celery_master_app, is_duplicate_task
from src.versions.v1.routes.question import get_elasticsearch


@celery_master_app.task(name="celery_tasks.workers.main.task_elastic_push")
def task_elastic_push():
    try:
        task_status = is_duplicate_task(task_name="celery_tasks.workers.main.task_elastic_push")
        if not task_status:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(_task_elastic_push())
    except Exception as Ex:
        print(str(Ex))
    finally:
        clear_db_session()
    return None


async def _task_elastic_push():
    """task to push in elastic"""
    es = get_elasticsearch()
    ElasticSearchController(es).push_document_incremental(_id=None)
