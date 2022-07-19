from apscheduler.schedulers.blocking import BlockingScheduler
import lstm_bot_heroku


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)
def job():
    print('This job is run every minute.')
    lstm_bot_heroku.trade()


sched.start()
