from celery.decorators import task
import time


@task
def sendmail(email):
    print('start send email to %s' % email)
    time.sleep(5)  # 休息5秒
    print('success')
    return True


# myproject是当前django的项目名
from myproject import celery_app
import time


@celery_app.task
def sendmail(email):
    print('start send email to %s' % email)
    time.sleep(5)  # 休息5秒
    print('success')
    return True


'''
from celery import task
from time import sleep


@task()
def Task_A(message):
    Task_A.update_state(state='PROGRESS', meta={'progress': 0})
    sleep(10)
    Task_A.update_state(state='PROGRESS', meta={'progress': 30})
    sleep(10)
    return message


def get_task_status(task_id):
    task = Task_A.AsyncResult(task_id)

    status = task.state
    progress = 0

    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.info['progress']

    return {'status': status, 'progress': progress}
'''

#定时任务
from celery.task.schedules import crontab
from celery.decorators import periodic_task

#每分钟执行一次
#http://docs.celeryproject.org/en/master/userguide/periodic-tasks.html
@periodic_task(run_every=crontab())
def some_task():
    print('periodic task test!!!!!')
    time.sleep(5)
    print('success')
    return True

#@periodic_task(run_every=10) ---20秒执行一次
#@periodic_task(run_every=datetime.timedelta(hours=1, minutes=15, seconds=40))
#具体时间段
#具体时间点
#crontab
#minute：分钟，范围0-59；
#hour：小时，范围0-23；
#day_of_week：星期几，范围0-6。以星期天为开始，即0为星期天。这个星期几还可以使用英文缩写表示，例如“sun”表示星期天；
#day_of_month：每月第几号，范围1-31；
#month_of_year：月份，范围1-12
#crontab(minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*')
#例如crontab(minute=15)每小时的15分执行一次

# 每2个小时中每分钟执行1次任务
crontab(hour='*/2')

# 每3个小时的0分时刻执行1次任务
# 即[0,3,6,9,12,15,18,21]点0分
crontab(minute=0, hour='*/3')

# 每3个小时或8点到12点的0分时刻执行1次任务
# 即[0,3,6,9,12,15,18,21]+[8,9,10,11,12]点0分
crontab(minute=0, hour='*/3,8-12')

# 每个季度的第1个月中，每天每分钟执行1次任务
# 月份范围是1-12，每3个月为[1,4,7,10]
crontab(month_of_year='*/3')

# 每月偶数天数的0点0分时刻执行1次任务
crontab(minute=0, hour=0, day_of_month='2-31/2')

# 每年5月11号的0点0分时刻执行1次任务
crontab(0, 0, day_of_month='11', month_of_year='5')
