import re,datetime

def from_utc(utcTime,fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    """
    Convert UTC time string to time.struct_time
    """
    # change datetime.datetime to time, return time.struct_time type
    return datetime.datetime.strptime(utcTime, "%Y,%m")

print from_utc("2007-03-04T21:08:12.123Z")
