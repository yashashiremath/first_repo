import datetime

now = datetime.datetime.now()
then = now - datetime.timedelta(hours=24)
print(then.timestamp())