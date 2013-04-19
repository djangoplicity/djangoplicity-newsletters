from datetime import datetime

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, FieldError
from django.http import Http404

from djangoplicity.archives.contrib.queries import CategoryQuery
from djangoplicity.newsletters.models import Newsletter

if settings.USE_I18N:
	from django.utils import translation


def category_extra_templates(model, query, query_name, query_data):
	if 'category' in query_data:
		return ['newsletters/newsletter_%s_list.html' % query_data['category'].slug]


class NewsletterCategoryQuery(CategoryQuery):
	"""
	"""
	def __init__(self, *args, **kwargs):
		defaults = {
			'extra_templates': category_extra_templates,
		}
		defaults.update(kwargs)
		super(NewsletterCategoryQuery, self).__init__(*args, **defaults)

	def queryset( self, model, options, request, stringparam=None, **kwargs ):

		if not stringparam:
			raise Http404

		#
		# Find category
		#
		categorymodel = self._get_categorymodel( model, self.relation_field )

		try:
			category = categorymodel.objects.get( **{ self.url_field: stringparam } )
		except categorymodel.DoesNotExist:
			# URL of non existing category specified.
			raise Http404
		except FieldError:
			raise ImproperlyConfigured( 'URL field does not exist on category model.' )
		except AttributeError:
			raise ImproperlyConfigured( 'Related query set attribute %s_set does not exist on category model.' % model._meta.module_name )

		#if stringparam in self.featured:
		#	print "featured"

		#
		# Select archive items in category
		#
		if settings.USE_I18N:
			lang = translation.get_language()
			qs = Newsletter.objects.language(lang).filter(type=category)
		else:
			qs = Newsletter.objects.filter(type=category)

		# Filter out non-sent Newsletters
		now = datetime.now()
		qs = self._filter_datetime_by_fieldname(qs, now, 'send', False, False)

		return ( qs, { 'category': category } )