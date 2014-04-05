from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson as Json
from django.conf import settings
from django.utils.importlib import import_module
from news_explorer.models import File, Person, Organization, Location, Article

def index(request):
    context = {}
    return render(request, 'news_explorer/index.html', context)

def new(request):
    context = {}
    return render(request, 'news_explorer/new.html', context)

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

def initiate(request):
    if request.method == 'GET':
        if request.GET["location"]:
            L = Location.objects.values('name').distinct()
            response = HttpResponse(Json.dumps(str(L), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        if request.GET["person"]:
            P = Person.objects.values('name').distinct()
            response = HttpResponse(Json.dumps(str(P), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        if request.GET["organization"]:
            O = Organization.objects.values('name').distinct()
            response = HttpResponse(Json.dumps(str(O), default=jdefault, indent=4), content_type="application/json",
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
            name = request.GET.get('person', '')
            P = Person.objects.extra(where=['name=%s'], params=[name]).values()
            response = HttpResponse(Json.dumps(str(P), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response
        elif request.GET["organization"]:
            name = request.GET.get('organization', '')
            O = Organization.objects.extra(where=['name=%s'], params=[name]).values()
            response = HttpResponse(Json.dumps(str(O), default=jdefault, indent=4), content_type="application/json",
                                    mimetype="application/json").content
            return response

    '''if request.GET["location"] and request.GET["person"] and request.GET["organization"]:
        f = File.objects.values()
        response_data = f
        response = HttpResponse(Json.dumps(str(f), default=jdefault, indent=4), content_type="application/json",
                                mimetype="application/json")
        return response

    elif request.GET["person"] and request.GET["location"]:
        return response
    elif request.GET["organization"] and request.GET["location"]:
        return response
    elif request.GET["organization"] and request.GET["person"]:
        return response'''