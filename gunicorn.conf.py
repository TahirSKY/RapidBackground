# Gunicorn configuration file
import multiprocessing

# Worker Options
workers = 2  # Fixed number of workers for better memory management
worker_class = 'gthread'  # Use threads for better I/O handling
threads = 4  # Number of threads per worker
max_requests = 100  # Restart workers after this many requests
max_requests_jitter = 10  # Add randomness to max_requests

# Logging Options
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Process Naming
proc_name = 'rapidbg'

# Timeout Configuration
timeout = 300  # 5 minutes for long image processing
keepalive = 24
graceful_timeout = 30

# Server Mechanics
preload_app = True
worker_tmp_dir = '/dev/shm'  # Use memory for temp files
forwarded_allow_ips = '*'  # Trust X-Forwarded-* headers

# Server Socket
bind = "0.0.0.0:10000"  # Default Render port

# Resource Management
worker_connections = 1000
limit_request_line = 4096
limit_request_fields = 100
