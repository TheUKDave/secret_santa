from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
ADMINS = (('David Downes', 'github@theukdave.com'),)

MIDDLEWARE += [
    'santa.middleware.IpRestrictionMiddleware',
]

RESTRICT_IPS = os.environ.get('RESTRICT_IPS', '').lower() in ['true', 'yes', '1']

allowed_ips = os.environ.get('ALLOWED_IPS', '')
allowed_ip_ranges = os.environ.get('ALLOWED_IP_RANGES', '')

# ALLOWED_IPS/_IP_RANGES should be a comma-separated list of ip address or network ranges
ALLOWED_IPS = allowed_ips.split(',') if allowed_ips != '' else []
ALLOWED_IP_RANGES = allowed_ip_ranges.split(',') if allowed_ip_ranges != '' else []
