import celery
app = celery.Celery('example')

@app.task
def my_background_task(arg1, arg2):
    # some long running task here
    print(" ### I am a background task ### ")
    return True
