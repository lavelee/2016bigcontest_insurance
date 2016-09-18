import datetime
def timestamp_to_days(timestamp, bottom=datetime.date(1995,1,1)):
    return (timestamp-bottom).total_seconds()/3600/24
a=datetime.date(1998, 1, 31)
print(timestamp_to_days(a))