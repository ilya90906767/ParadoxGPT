from django.core.management.base import BaseCommand
from fetcher.fetcher_main import main
from fetcher.fetcher_main import client  

import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = "Bot polling"

    def handle(self, *args, **options):
        print('Fetcher polling')
        try:
            main()
        except Exception as e:
            logging.error(f"Error running main function: {e}")