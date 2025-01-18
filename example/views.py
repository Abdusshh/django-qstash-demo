# example/views.py
from datetime import datetime
from os import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .tasks import sample_task
import logging

logger = logging.getLogger(__name__)

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Django QStash Example</h1>
            <p>Current time: {now}</p>
            <p><a href="/trigger-task/">Trigger a new task</a></p>
        </body>
    </html>
    '''
    return HttpResponse(html)

@csrf_exempt
def trigger_task_view(request):
    """
    Renders a form that lets the user choose between `.delay()`
    and `.apply_async(countdown=...)` and also specify a message.
    """
    if request.method == "POST":
        message = request.POST.get("message", "")
        execution_type = request.POST.get("execution_type", "delay")
        countdown_str = request.POST.get("countdown", "0")  # defaults to 0

        logger.info(f"Message: {message}")
        logger.info(f"Message type: {type(message)}")
        logger.info(f"Execution Type: {execution_type}")
        logger.info(f"Countdown: {countdown_str}")

        # Convert countdown to an integer (handle non-integer input gracefully)
        try:
            countdown_val = int(countdown_str)
        except ValueError:
            countdown_val = 0

        # Decide which method to call
        if execution_type == "delay":
            sample_task.delay(message)
        else:
            # apply_async with a countdown
            sample_task.apply_async(args=[message], countdown=countdown_val)

        return redirect("/task-triggered-success/")

    return render(request, "example/pick_delay.html")

def task_triggered_success_view(request):
    """
    Simple success page to inform the user that the task was queued.
    """
    return render(request, "example/task_triggered_success.html")