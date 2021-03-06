===================
django-trusted-html
===================

Django-trusted-html will make your html correct, pretty and safe.
-----------------------------------------------------------------

Usage lyrics
============

Suppose that some users can post content to your site.
And you want to allow them to post formatted text, images, tables and videos.
The best way is using HTML as native format and WYSIWYG editor as user interface.
So your users will create content easy and will be happy.
They will be able to copy-and-paste content from other sites or GUI-Editors.
But you can become unhappy. Your site can looks not homogeneous because of
different font-families, colors, indents that will come with copy-and-pasted content.
Also you can want to protect your site from JavaScript injections.
In this way you might want to use django-trusted-html.


Sanitizing
----------

This is application for sanitizing HTML from:

1. javascript injections
2. objectionable CSS styles
3. objectionable tags
4. objectionable or inaccessible links, images and embedded objects

For example you can:

1. remove scripts from user`s content posted to your site
2. remove user-specified fonts and colors to make your site looks pretty
3. allow user to post video for example only from 'youtube.com'
4. disable images arranged not on your own site


Valid HTML
----------

This is application for making valid HTML:

1. remove incorrect tags, attributes, css-properties and css-values not allowed to this property
2. check and remove broken link, and do some more things with them

For example you can:

1. make all your content w3c valid
2. remove broken links to other sites
3. remove host name from links to you site.


Custom
------

You can:

1. choose one of presets
2. specify settings of validation
3. customize rules of validation

Installation:
=============

1. Put ``trustedhtml`` in to your ``INSTALLED_APPS`` in your ``settings.py`` within your django project.

2. Sync your database::

    ./manage.py syncdb

3. Customize settings in your ``settings.py``.

To learn more about settings read ``trustedhtml/settings.py``. 


Requirements:
=============

Django 1.3+ is required.
For Django < 1.3 please check out django-trusted-html 0.1.2.


Usage:
======

In your models:
---------------

1. You can use TrustedField in your model ::

	from trustedhtml.fields import TrustedTextField

	class MyModel(models.Model):
	    html = TrustedTextField()

Also you can specify one of predefined validators ::

	from trustedhtml.rules import full, normal, pretty
	from trustedhtml.fields import TrustedTextField

	class MyModel(models.Model):
	    html = TrustedTextField(validator=pretty)

``trustedhtml.rules.full`` rule will safe all html tags and css style described by w3c.

``trustedhtml.rules.normal`` rule will remove dangerous html element, or elements that can break you design.

``trustedhtml.rules.pretty`` rule also will remove colors, fonts, aligns, margins and other css and html attributes.

By the way, if you have django-tinymce in INSTALLED_APPS, than you can use TrustedHTMLField.

2. You can validate html before it will be saved::

	from trustedhtml.rules import pretty

	class MyModel(models.Model):
	    html = models.TextField()
	    def save(self, *args, **kwargs):
	        self.html = pretty.validate(self.html)
	        super(MyModel, self).save(*args, **kwargs)

Or::

	from trustedhtml.rules import pretty
	from someapp.models import SomeModel

	def content_save(sender, instance, **kwargs):
	    instance.content = pretty.validate(instance.content)

	pre_save.connect(content_save, sender=SomeModel)

3. You can validate html by using widget::

	from django import forms
	from trustedhtml.widgets import TrustedTextarea

	class FormField(forms.TextField):
		widget = TrustedTextarea

If you are using django-pages-cms, you can just use TrustedWidget in templates::

	{% placeholder main_content with TrustedTextarea %}

Or for older versions of django-pages-cms::

	{% placeholder main_content with trustedhtml.widgets.TrustedTextarea %}
	
Also if you are using TinyMCE::

    {% placeholder main_content with trustedhtml.widgets.TrustedTinyMCE %}

Or for older versions of django-pages-cms::

    {% placeholder main_content with TrustedTinyMCE %}
    

4. You can just ask trusted html to validate specified fields in specified models.

In some application::

	class SomeModel(models.Model):
		name = models.CharField(max_length=100)
	    description = models.TextField()

In your ``settings.py``::

	TRUSTEDHTML_MODELS = [
	    {
	        'model': 'someapp.models.SomeModel',
	        'fields': ['description', ],
	    },
    ]

Changelog:
----------

* 0.1.0 - Initial release
* 0.1.1 - Allow <iframe> elements from trusted sits (for youtube movies)
* 0.1.2 - Setup for RedsolutionCMS execute in postmake and write settings in the end of settings.py
* 0.2.0 - Django 1.6 compatibility.

Classifiers:
-------------

`Content plugins`_

.. _`Content plugins`: http://www.redsolutioncms.org/classifiers/content