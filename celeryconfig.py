"""
Celery configuration file for setting up the message broker and result backend.
"""

# Set the URL for the Redis broker
broker_url = 'redis://redis:6379/0'
# Set the URL for the Redis backend
result_backend = 'redis://redis:6379/0'
