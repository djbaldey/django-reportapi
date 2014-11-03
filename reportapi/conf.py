# -*- coding: utf-8 -*-
#
#  reportapi/conf.py
#  
#  Copyright 2014 Grigoriy Kramarenko <root@rosix.ru>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import unicode_literals, print_function, division
from django.utils.encoding import smart_text, python_2_unicode_compatible
from django.utils import six

from django.conf import settings
from django import VERSION as django_version
from reportapi import __version__ as reportapi_version
from quickapi import __version__ as quickapi_version

SITE_ID = settings.SITE_ID
DEBUG   = settings.DEBUG

DJANGO_VERSION          = '.'.join([str(x) for x in django_version[:2]])
REPORTAPI_VERSION       = reportapi_version
QUICKAPI_VERSION        = quickapi_version
REPORTAPI_DEBUG = getattr(settings, 'REPORTAPI_DEBUG', settings.DEBUG)
REPORTAPI_ROOT = getattr(settings, 'REPORTAPI_ROOT', '%s/reports/' % settings.MEDIA_ROOT.rstrip('/'))
REPORTAPI_URL  = getattr(settings, 'REPORTAPI_URL',  '%s/reports/' % settings.MEDIA_URL.rstrip('/'))
REPORTAPI_ENABLE_THREADS = getattr(settings, 'REPORTAPI_ENABLE_THREADS', False)
REPORTAPI_CODE_HASHLIB = getattr(settings, 'REPORTAPI_CODE_HASHLIB', 'md5')
REPORTAPI_UPLOAD_HASHLIB = getattr(settings, 'REPORTAPI_UPLOAD_HASHLIB', 'md5')
REPORTAPI_FILES_UNIDECODE = getattr(settings, 'REPORTAPI_FILES_UNIDECODE', False)
REPORTAPI_LANGUAGES = getattr(settings, 'REPORTAPI_LANGUAGES', ['en', 'ru'])

REPORTAPI_UNOCONV_TO_ODF = getattr(settings, 'REPORTAPI_UNOCONV_TO_ODF', False)
REPORTAPI_UNOCONV_TO_PDF = getattr(settings, 'REPORTAPI_UNOCONV_TO_PDF', True)

REPORTAPI_BRAND_TEXT = getattr(settings, 'REPORTAPI_BRAND_TEXT', '')

AUTH_USER_MODEL  = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Header(object):
    min_height      = getattr(settings, 'REPORTAPI_HEADER_MIN_HEIGHT', '0.1cm')
    margin_top      = getattr(settings, 'REPORTAPI_HEADER_MARGIN_TOP', '0cm')
    margin_bottom   = getattr(settings, 'REPORTAPI_HEADER_MARGIN_BOTTOM', '0cm')
    margin_left     = getattr(settings, 'REPORTAPI_HEADER_MARGIN_LEFT', '0cm')
    margin_right    = getattr(settings, 'REPORTAPI_HEADER_MARGIN_RIGHT', '0cm')
    dynamic_spacing = getattr(settings, 'REPORTAPI_HEADER_DYNAMIC_SPACING', 'false')
    auto_height     = getattr(settings, 'REPORTAPI_HEADER_AUTO_HEIGHT', 'false')

class Footer(object):
    min_height    = getattr(settings, 'REPORTAPI_FOOTER_MIN_HEIGHT', '1.2cm')
    margin_top    = getattr(settings, 'REPORTAPI_FOOTER_MARGIN_TOP', '0.5cm')
    margin_bottom = getattr(settings, 'REPORTAPI_FOOTER_MARGIN_BOTTOM', '0cm')
    margin_left   = getattr(settings, 'REPORTAPI_FOOTER_MARGIN_LEFT', '0cm')
    margin_right  = getattr(settings, 'REPORTAPI_FOOTER_MARGIN_RIGHT', '0cm')
    border_top    = getattr(settings, 'REPORTAPI_FOOTER_BORDER_TOP', '0.002cm solid #000000')

class Page(object):
    style_name    = getattr(settings, 'REPORTAPI_PAGE_STYLE_NAME', 'A4')
    width         = getattr(settings, 'REPORTAPI_PAGE_WIDTH', '21cm')
    height        = getattr(settings, 'REPORTAPI_PAGE_HEIGHT', '29.7cm')
    margin_top    = getattr(settings, 'REPORTAPI_PAGE_MARGIN_TOP', '0.6cm')
    margin_bottom = getattr(settings, 'REPORTAPI_PAGE_MARGIN_BOTTOM', '0.6cm')
    margin_left   = getattr(settings, 'REPORTAPI_PAGE_MARGIN_LEFT', '2.0cm')
    margin_right  = getattr(settings, 'REPORTAPI_PAGE_MARGIN_RIGHT', '0.6cm')
    num_format    = getattr(settings, 'REPORTAPI_PAGE_NUM_FORMAT', '1')
    print_orientation   = getattr(settings, 'REPORTAPI_PAGE_PRINT_ORIENTATION', 'portrait')
    footnote_max_height = getattr(settings, 'REPORTAPI_PAGE_FOOTNOTE_MAX_HEIGHT', '0cm')

    header = Header()
    footer = Footer()

    def checked(self):
        w = float(self.width.replace('cm', ''))
        h = float(self.height.replace('cm', ''))
        if self.print_orientation == 'landscape' and h > w:
            self.width, self.height = self.height, self.width
        elif h < w and self.print_orientation == 'portrait':
            self.print_orientation == 'landscape'
        return self
