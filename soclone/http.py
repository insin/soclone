from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson

class JsonResponse(HttpResponse):
    """From http://www.djangosnippets.org/snippets/154/"""
    def __init__(self, obj):
        if isinstance(obj, QuerySet):
            content = serialize('json', obj)
        else:
            content = simplejson.dumps(obj)
        super(JsonResponse, self).__init__(content, mimetype='application/json')
