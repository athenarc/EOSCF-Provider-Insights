import logging
from multiprocessing import Process

from apscheduler.schedulers.blocking import BlockingScheduler
from health.monitoring import cronitor_monitoring


def init_scheduler():
    scheduler = BlockingScheduler()

    scheduler.add_job(
        scheduled_heartbeat, 'cron',
        minute="*/5"
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def scheduled_heartbeat():
    logging.info("Sending heartbeat...")
    cronitor_monitoring.send_heartbeat_message()


def start_scheduler_process():
    p = Process(target=init_scheduler)
    logging.info("Starting process...")
    p.start()
