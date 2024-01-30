workers = 4

bind = "0.0.0.0:8000"

app = "backend.asgi:application"

worker_class = "uvicorn.workers.UvicornWorker"

timeout = 120

daemon = False