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

from djangoplicity.actions.plugins import ActionPlugin


class MailmanAction(ActionPlugin):
	"""
	An action plugin is a configureable celery task,
	that can be dynamically connected to events in the system.
	"""
	action_parameters = [ 
		('list_name', 'Mailman list name - must be defined in djangoplicity', 'str'),
	]
	abstract = True
	
	@classmethod
	def get_arguments(cls, conf, *args, **kwargs):
		"""
		Parse incoming arguments. Email lookup:
		1) if an 'email' kwarg is provided, then the value is used.
		2) otherwise 
		"""
		email = None
		if 'email' in kwargs:
			email = kwargs['email']
		else:
			for v in kwargs.values():
				if hasattr( v, 'email' ):
					email = v.email
					break

		return ( [], { 'email' : email } )

	
	def _get_list(self, list_name):
		from djangoplicity.mailinglists.models import List
		return List.objects.get( name=list_name ) 


class MailmanSubscribeAction(MailmanAction):
	action_name = 'Mailman subscribe'
	
	def run(self, conf, email=None):
		"""
		Subscribe to mailman list
		"""
		if email:
			list = self._get_list( conf['list_name'] )
			list.subscribe( email=email, async=False )
			self.get_logger().info("Subscribed %s to mailman list %s" % ( email, list.name ) )
		
		
class MailmanUnsubscribeAction(MailmanAction):
	action_name = 'Mailman unsubscribe'
	
	def run(self, conf, email=None):
		"""
		Unsubscribe from mailman list
		"""
		if email:
			list = self._get_list( conf['list_name'] )
			list.unsubscribe( email=email, async=False )
			self.get_logger().info("Unsubscribed %s to mailman list %s" % ( email, list.name ) )
		
class MailmanUpdateAction( MailmanAction ):
	action_name = 'Mailman update subscription'
	
	@classmethod
	def get_arguments(cls, conf, *args, **kwargs):
		return ( args, kwargs )
	
	def run(self, conf, from_email=None, to_email=None, **kwargs ):
		"""
		Email address was updated so change subscriber
		"""
		if from_email != to_email and from_email is not None and to_email is not None:
			# from/to email can be empty but not none (empty basically means unsubscribe).
			list = self._get_list( conf['list_name'] )
			if from_email != '':
				list.unsubscribe( email=from_email, async=False )
				self.get_logger().info( "Unsubscribed %s to mailman list %s" % ( from_email, list.name ) )
			if to_email != '':
				list.subscribe( email=to_email, async=False )
				self.get_logger().info( "Subscribed %s to mailman list %s" % ( to_email, list.name ) )


class MailmanSyncAction( MailmanAction ):
	action_name = 'Mailman synchronize'
	action_parameters = MailmanAction.action_parameters + [ 
		('remove_existing', 'Remove any mailman subscriber not defined in djangoplicity.', 'bool'),
	]
	
	@classmethod
	def get_arguments( cls, conf, *args, **kwargs ):
		for v in kwargs.values():
			if hasattr( v, 'get_emails' ) and callable( v.get_emails ):
				module = v.__class__.__module__
				klass = v.__class__.__name__
				pk = v.pk
				break

		return ( [], { 'module' : module, 'klass' : klass, 'pk' : pk } )
	
	
	def _get_emails( self, module, klass, pk ):
		"""
		Get the list of emails to synchronize
		"""
		m = __import__( module, globals(), locals(), [klass], -1 )
		cls = getattr( m, klass )
		obj = cls.objects.get( pk = pk )
		return obj.get_emails()

	def run( self, conf, module=None, klass=None, pk=None ):
		"""
		"""
		emails = self._get_emails()
		mlist = self._get_list( conf['list_name'] )
		mlist.update_subscribers( emails )
		mlist.push( remove_existing=conf['remove_existing'] )



MailmanSubscribeAction.register()
MailmanUnsubscribeAction.register()
MailmanUpdateAction.register()
MailmanSyncAction.register()