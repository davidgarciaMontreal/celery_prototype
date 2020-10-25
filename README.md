# Launch
## pre steps setup backend

```docker-compose -f docker-compose-yml up -d ```

## Running
Terminal one:

```celery -A tasks  worker --loglevel=INFO```

Terminal two:

```python3  task_dispatcher.py  --parallel no --number 4```
## Logs
