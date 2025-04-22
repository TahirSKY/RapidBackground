# Gunicorn configuration file
import multiprocessing
import os

# Set OpenMP environment variables
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['VECLIB_MAXIMUM_THREADS'] = '1'

# Worker Options
workers = 2  # Fixed number of workers for better memory management
worker_class = 'sync'  # Use sync workers to avoid threading issues
max_requests = 50  # Restart workers more frequently to prevent memory buildup
max_requests_jitter = 10  # Add randomness to max_requests

# Logging Options
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Process Naming
proc_name = 'rapidbg'

# Timeout Configuration
timeout = 120  # Reduce timeout to 2 minutes
keepalive = 24
graceful_timeout = 30

# Server Mechanics
preload_app = True
worker_tmp_dir = '/dev/shm'  # Use memory for temp files
forwarded_allow_ips = '*'  # Trust X-Forwarded-* headers

# Server Socket
bind = "0.0.0.0:10000"  # Default Render port

# Resource Management
worker_connections = 500  # Reduce connections to save memory
limit_request_line = 4096
limit_request_fields = 100

# Memory Management
max_requests_jitter = 10
worker_abort_on_error = True  # Restart workers on errors
