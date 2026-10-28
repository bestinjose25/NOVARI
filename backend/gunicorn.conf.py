import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = 1
threads = 2
# Photo emails are synchronous; a durable email queue is a future improvement.
timeout = 300
graceful_timeout = 300
accesslog = '-'
errorlog = '-'
# Exclude query strings and submitted content from access logs.
access_log_format = '%(h)s %(m)s %(U)s %(s)s %(L)s'
