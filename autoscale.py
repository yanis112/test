from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def job():
    print 'This job is run every minute.'


sched.start()
