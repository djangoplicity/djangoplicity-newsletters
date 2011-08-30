# -*- coding: utf-8 -*-
#
# djangoplicity-newsletters
# Copyright (c) 2007-2011, European Southern Observatory (ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#	* Redistributions of source code must retain the above copyright
#	  notice, this list of conditions and the following disclaimer.
#
#	* Redistributions in binary form must reproduce the above copyright
#	  notice, this list of conditions and the following disclaimer in the
#	  documentation and/or other materials provided with the distribution.
#
#	* Neither the name of the European Southern Observatory nor the names 
#	  of its contributors may be used to endorse or promote products derived
#	  from this software without specific prior written permission.
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

"""
Djangoplicity Newsletter
"""

from django import forms
from djangoplicity.newsletters.models import Newsletter
from django.contrib.admin import widgets

from django.core.validators import validate_email

class MultiEmailField( forms.CharField ):
	def to_python( self, value ):
		"""
		Normalize data to a list of strings.
		"""
		# Return an empty list if no input was given.
		if not value:
			return []
		return [x.strip() for x in value.split( ',' )]

	def validate( self, value ):
		"""
		Check if value consists only of valid emails.
		"""
		super( MultiEmailField, self ).validate( value )

		for email in value:
			validate_email( email )


class GenerateNewsletterForm( forms.ModelForm ):
	class Meta:
		model = Newsletter
		fields = [ 'type', 'start_date', 'end_date' ]
		widgets = {
			'start_date': widgets.AdminSplitDateTime(),
			'end_date': widgets.AdminSplitDateTime(),
		}


class TestEmailsForm( forms.Form ):
	emails = MultiEmailField( max_length=255 )
	
class SendNewsletterForm( forms.Form ):
	send_now = forms.BooleanField()

