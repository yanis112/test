from apscheduler.schedulers.blocking import BlockingScheduler
import lstm_bot_heroku
from lstm_bot_heroku import trade

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=30)
def job():
    print('This job is run every minute.')
    trade()


sched.start()
