__author__ = 'hjdesai2'
import urllib2
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson as Json
from django.conf import settings
from django.utils.importlib import import_module
from news_explorer.models import File, Person, Organization, Location, Article
request = HttpRequest()
response_data ={}

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

def initiate():
    L = Location.objects.values()
    response = HttpResponse(Json.dumps(str(L), default=jdefault, indent=4),content_type="application/json",
                            mimetype="application/json").content
    return response


def getJson(request):
    if request.method == 'GET':
        if request.GET["location"]:
            name = request.GET.get('location', '')
            L = Location.objects.extra(where=['name=%s'], params=[name]).values()
            response = HttpResponse(Json.dumps(str(L), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        elif request.GET["person"]:
            name = request.GET['person']
            P = Person.objects.extra(where=['name=%s'], params=[name]).values()
            response = HttpResponse(Json.dumps(str(P), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        elif request.GET["organization"]:
            name = request.GET['organization']
            O = Organization.objects.extra(where=['name=%s'], params=[name]).values()
            response = HttpResponse(Json.dumps(str(O), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response

    if request.GET["location"] and request.GET["person"] and request.GET["organization"]:
        f = File.objects.values()
        response_data = f
        response = HttpResponse(Json.dumps(str(f), default=jdefault, indent=4), content_type="application/json",
                                mimetype="application/json").content
        return response

    elif request.GET["person"] and request.GET["location"]:
        return response
    elif request.GET["organization"] and request.GET["location"]:
        return response
    elif request.GET["organization"] and request.GET["person"]:
        return response




