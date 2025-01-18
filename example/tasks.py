import datetime
from django_qstash import stashed_task

@stashed_task
def sample_task(message: str):
    """
    Simple task that prints the current time + the message.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now_str}] sample_task triggered. Message: {message}")
    return f"Done sample_task with message: {message}"