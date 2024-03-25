#!/usr/bin/env python3
import asyncio
import functions_framework
from google.cloud.logging import Client as logClient
from bot import telegramma

@functions_framework.http
def entrypoint(request):
    """This function is called as cloud function entrypoint"""
    client = logClient().setup_logging()
    return asyncio.run(telegramma(request))

