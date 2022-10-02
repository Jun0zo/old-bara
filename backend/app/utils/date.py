from pytz import timezone
from datetime import datetime


def get_now_datetime():
    return datetime.now(timezone("Asia/Seoul"))
