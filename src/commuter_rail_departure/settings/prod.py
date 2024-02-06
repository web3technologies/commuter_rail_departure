from .settings import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_WHITELIST = [
    'https://commuter-rail-departure.vercel.app',
    "https://commuter-rail-departure-git-develop-web3technologies.vercel.app"
]