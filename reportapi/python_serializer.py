# -*- coding: utf-8 -*-
"""
###############################################################################
# Copyright 2014 Grigoriy Kramarenko.
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
from StringIO import StringIO
from types import MethodType
from django.db import models
from django.utils.encoding import smart_unicode, is_protected_type
from django.core.paginator import Page
from django.core.serializers.python import Serializer as OrignSerializer

def page_range_dots(page, on_each_side=3, on_ends=2, dot='.'):
    number    = page.number
    num_pages = page.paginator.num_pages
    page_range = page.paginator.page_range
    #~ print 0, page_range
    if num_pages > 9:
        page_range = []
        if number > (on_each_side + on_ends):
            page_range.extend(range(1, on_each_side))
            page_range.append(dot)
            page_range.extend(range(number +1 - on_each_side, number + 1))
            #~ print 1, page_range
        else:
            page_range.extend(range(1, number + 1))
            #~ print 2, page_range
        if number < (num_pages - on_each_side - on_ends + 1):
            page_range.extend(range(number + 1, number + on_each_side))
            page_range.append(dot)
            page_range.extend(range(num_pages - on_ends +1, num_pages+1))
            #~ print 3, page_range
        else:
            page_range.extend(range(number + 1, num_pages+1))
    return page_range

class SerializerWrapper(object):
    """ Обёртка вокруг базовых классов Django.
        Переопределяет их методы.
    """
    def handle_field(self, obj, field):
        value = field._get_val_from_obj(obj)
        self._current[field.name] = value
        return value

    def handle_property(self, obj, name):
        value = getattr(obj, name)
        if callable(value):
            value = value()
        if isinstance(value, models.Model):
            app, model = smart_unicode(value._meta).split('.')
            value = {
                self.unicode_key: smart_unicode(value),
                'pk': value.pk,
                'app': app,
                'model': model,
            }
        self._current[name] = value
        return value

    def handle_fk_field(self, obj, field):
        if obj.pk:
            related = getattr(obj, field.name)
            if related:
                value = (related.pk, smart_unicode(related))
            else:
                value = None
        else:
            value = getattr(obj, field.get_attname())
            rel_model = field.rel.to
            try:
                related = rel_model._default_manager.get(pk=value)
                value = (related.pk, smart_unicode(related))
            except:
                value = None

        self._current[field.name] = value
        return value

    def handle_m2m_field(self, obj, field):
        value = []
        if obj.pk and field.rel.through._meta.auto_created:
            m2m_value = lambda value: (value.pk, smart_unicode(value))
            value = [m2m_value(related)
                            for related in getattr(obj, field.name).iterator()]

        self._current[field.name] = value
        return value

    def serialize_objects(self, objects, **options):
        """
        Практически в точности копирует оригинальный метод serialize,
        но не запускает в конце метод окончания сериализации
        """

        self.stream = options.pop("stream", StringIO())
        self.attrs = options.pop("attrs", [])
        self.unicode_key = options.pop("unicode_key", '__unicode__')
        # Простой список для <select> в HTML: ключ и сроковое представление
        self.simple_select_list = options.pop("simple_select_list", False)
        if self.simple_select_list:
            self.attrs = []

        self.start_serialization()

        if isinstance(objects, models.Model):
            opts = objects._meta
            objects = [objects]
        else:
            opts = objects.model._meta
            objects = objects.select_related()

        local_fields = [x.name for x in opts.local_fields]
        many_to_many = [x.name for x in opts.many_to_many]

        for obj in objects:

            self.start_object(obj)

            for attr in self.attrs:
                if attr in local_fields:
                    field = opts.local_fields[local_fields.index(attr)]
                    if field.rel is None:
                        self.handle_field(obj, field)
                    else:
                        self.handle_fk_field(obj, field)
                elif attr in many_to_many:
                    field = opts.many_to_many[many_to_many.index(attr)]
                    self.handle_m2m_field(obj, field)
                elif not attr in ('pk', '__unicode__'):
                    self.handle_property(obj, attr)

            self.end_object(obj)

        return self.objects

    def serialize(self, objects, **options):
        """
        Serialize a Model insnance, QuerySet or page of Paginator.
        """
        if isinstance(objects, Page):
            result = {}
            wanted = ("end_index", "has_next", "has_other_pages", "has_previous",
                    "next_page_number", "number", "start_index", "previous_page_number")
            for attr in wanted:
                v = getattr(objects, attr)
                if isinstance(v, MethodType):
                    try:
                        result[attr] = v()
                    except:
                        result[attr] = None
                elif isinstance(v, (str, int)):
                    result[attr] = v
            result['count']       = objects.paginator.count
            result['num_pages']   = objects.paginator.num_pages
            result['per_page']    = objects.paginator.per_page
            result['page_range']  = page_range_dots(objects)
            result['object_list'] = self.serialize_objects(objects.object_list, **options)
            self.objects = result
        else:
            self.serialize_objects(objects, **options)

        self.end_serialization() # Окончательно сериализуем
        value = self.getvalue()

        if isinstance(objects, models.Model):
            return value[0]
        else:
            return value

    def start_object(self, obj):
        self._current = {}

    def end_object(self, obj):
        _unicode = ""
        try:
            _unicode = smart_unicode(obj)
        except:
            pass
        pk = smart_unicode(obj._get_pk_val(), strings_only=True)
        if self.simple_select_list:
            self._current = (pk, _unicode)
        else:
            self._current[self.unicode_key] = _unicode
            self._current["pk"] = pk
        self.objects.append(self._current)
        self._current = None

class Serializer(SerializerWrapper, OrignSerializer):
    """
    Serializes a QuerySet or page of Paginator to basic Python objects.
    """
    pass

def serialize(queryset, **options):
    """
    Serialize a queryset (or any iterator that returns database objects).
    """
    s = Serializer()
    s.serialize(queryset, **options)
    return s.getvalue()
