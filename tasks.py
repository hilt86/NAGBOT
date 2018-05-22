import celery
app = celery.Celery('example')

@app.task
def my_background_task(arg1, arg2):
    # some long running task here
    with app.app_context():
        print(" ### I am a background task ### ")
