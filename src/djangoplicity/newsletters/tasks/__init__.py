# -*- coding: utf-8 -*-
#
# djangoplicity-newsletters
# Copyright (c) 2007-2011, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the European Southern Observatory nor the names 
#      of its contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE
#

from celery.task import task

@task( name="newsletters.check_scheduled_tasks", ignore_result=True )
def check_scheduled_tasks():
	"""
	"""
	pass
	

@task( name="newsletters.send_scheduled_newsletter", ignore_result=True )
def send_scheduled_newsletter( newsletter_pk ):
	"""
	Task to start sending a scheduled newsletter   
	"""
	from djangoplicity.newsletters.models import Newsletter
	
	logger = send_scheduled_newsletter.get_logger()
	
	nl = Newsletter.objects.get( pk = newsletter_pk )
	
	logger.info("Starting to send scheduled newsletter %s" % newsletter_pk)
	
	nl._send()


@task( name="newsletters.send_newsletter", ignore_result=True )
def send_newsletter( newsletter_pk ):
	"""
	Task to start sending a newsletter  
	"""
	from djangoplicity.newsletters.models import Newsletter
	
	logger = send_newsletter.get_logger()
	
	nl = Newsletter.objects.get( pk = newsletter_pk )
	
	logger.info("Starting to send newsletter %s" % newsletter_pk)
	
	nl._send_now()
	
@task( name="newsletters.send_newsletter_test", ignore_result=True )
def send_newsletter_test( newsletter_pk, emails ):
	"""
	Task to start sending a newsletter  
	"""
	from djangoplicity.newsletters.models import Newsletter
	
	logger = send_newsletter.get_logger()
	
	nl = Newsletter.objects.get( pk = newsletter_pk )
	
	logger.info( "Starting to send test newsletter %s" % newsletter_pk )
	
	nl._send_test( emails )
	

@task( name="newsletters.schedule_newsletter", ignore_result=True )
def schedule_newsletter( newsletter_pk ):
	"""
	Task to schedule a newsletter for delivery.  
	"""
	from djangoplicity.newsletters.models import Newsletter
	
	logger = schedule_newsletter.get_logger()
	
	nl = Newsletter.objects.get( pk = newsletter_pk )
	
	logger.info("Scheduling newsletter %s" % newsletter_pk)
	
	nl._schedule()
	
@task( name="newsletters.unschedule_newsletter", ignore_result=True )
def unschedule_newsletter( newsletter_pk ):
	"""
	Task to unschedule a newsletter for delivery.
	"""
	from djangoplicity.newsletters.models import Newsletter
	
	logger = unschedule_newsletter.get_logger()
	
	nl = Newsletter.objects.get( pk = newsletter_pk )
	
	logger.info("Unscheduling newsletter %s" % newsletter_pk)
	
	nl._unschedule()		