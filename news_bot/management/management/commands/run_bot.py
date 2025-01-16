from django.core.management.base import BaseCommand
from bot.main_bot import main

import asyncio
import logging
import os
from dotenv import load_dotenv
load_dotenv()
    
class Command(BaseCommand):
    help = "Bot polling"
    
    def handle(self, *args, **options):
        print('Bot polling')
        logging.basicConfig(level=os.getenv("DJANGO_LOG_LEVEL", "WARNING"))
        asyncio.run(main())