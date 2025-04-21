# Gunicorn configuration file
import multiprocessing

# Worker Options
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
threads = 4

# Logging Options
accesslog = '-'
errorlog = '-'

# Process Naming
proc_name = 'rapidbg'

# Timeout Configuration
timeout = 300  # 5 minutes for long image processing
keepalive = 24

# Server Mechanics
preload_app = True

# Server Socket
bind = "0.0.0.0:10000"  # Default Render port
