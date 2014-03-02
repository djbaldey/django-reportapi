# -*- coding: utf-8 -*-
"""
###############################################################################
# Copyright 2012 Grigoriy Kramarenko.
###############################################################################
# This file is part of ReportAPI.
#
#    ReportAPI is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ReportAPI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ReportAPI.  If not, see <http://www.gnu.org/licenses/>.
#
# Этот файл — часть ReportAPI.
#
#   ReportAPI - свободная программа: вы можете перераспространять ее и/или
#   изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
#   в каком она была опубликована Фондом свободного программного обеспечения;
#   либо версии 3 лицензии, либо (по вашему выбору) любой более поздней
#   версии.
#
#   ReportAPI распространяется в надежде, что она будет полезной,
#   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
#   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
#   общественной лицензии GNU.
#
#   Вы должны были получить копию Стандартной общественной лицензии GNU
#   вместе с этой программой. Если это не так, см.
#   <http://www.gnu.org/licenses/>.
###############################################################################
"""
from django.conf import settings

SITE_ID = settings.SITE_ID
DEBUG   = settings.DEBUG

REPORTAPI_ROOT = getattr(settings, 'REPORTAPI_ROOT', '%s/reports/' % settings.MEDIA_ROOT.rstrip('/'))
REPORTAPI_URL  = getattr(settings, 'REPORTAPI_URL',  '%s/reports/' % settings.MEDIA_URL.rstrip('/'))
REPORTAPI_ENABLE_THREADS = getattr(settings, 'REPORTAPI_ENABLE_THREADS', False)
REPORTAPI_CODE_HASHLIB = getattr(settings, 'REPORTAPI_CODE_HASHLIB', 'md5')
REPORTAPI_UPLOAD_HASHLIB = getattr(settings, 'REPORTAPI_UPLOAD_HASHLIB', 'md5')
REPORTAPI_FILES_UNIDECODE  = getattr(settings, 'REPORTAPI_FILES_UNIDECODE', False)
AUTH_USER_MODEL  = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
AUTH_GROUP_MODEL = getattr(settings, 'AUTH_GROUP_MODEL', 'auth.Group')
#~ REPORTAPI_EXTERNAL_SUPPORT = getattr(settings, 'REPORTAPI_EXTERNAL_SUPPORT',  False)
#~ REPORTAPI_DEFAULT_TIMEOUT = getattr(settings, 'REPORTAPI_DEFAULT_TIMEOUT', 2)
