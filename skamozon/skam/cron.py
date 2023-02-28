import asyncio
import datetime
from django.core import management
from django.shortcuts import render, redirect
from skam.management.commands.bot import log_submit, log_submit_w, log_submit_y, log_user_action
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from skam.models import Link
from django.http import Http404
from skam.management.commands.bot import Command
from django.core.management import call_command



def starting_bot():
	call_command('bot')