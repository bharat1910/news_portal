__author__ = 'bharat'

from news_explorer.models import Location, ParentLocation
import requests

try:
    def insertParentLocation():
        locationToParentMap = {}
        parents = []
        parentsToIdMap = {}

        L = Location.objects.all()
        for l in L:
            print(l.name)
            locationToParentMap[l.name] = getParent(l.name)

            if locationToParentMap[l.name] not in parents:
                parents.append(locationToParentMap[l.name])

        for p in parents:
            pl = ParentLocation(name = p)
            pl.save()
            parentsToIdMap[p] =  ParentLocation.objects.latest('id').id

        for l in L:
            l.parentlocation_id = parentsToIdMap[locationToParentMap[l.name]]
            l.save()

    def getParent(location):
        try :
            (lat,lng) = getCoordinates(location)
            url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lng)+'&sensor=false'
            r = requests.get(url, auth=('user', 'pass'))
            res = r.json()
            res = convert(res)
            rows = res['results'][0]['address_components']
            count = len(rows)
            country = location
            for x in range(0,count):
                type_of_attr = str(rows[x]['types'])
                if 'country' in type_of_attr:
                    country = rows[x]['long_name']
            print country
            return country
        except:
            return location

    def getCoordinates(location):
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&sensor=true'
        r = requests.get(url, auth=('user', 'pass'))
        res = r.json()
        res = convert(res)
        lat = res['results'][0]['geometry']['location']['lat']
        lng = res['results'][0]['geometry']['location']['lng']
        print (lat,lng)
        return (lat,lng)

    def convert(input):
        if isinstance(input, dict):
            return {convert(key): convert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [convert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
except:
    print(SystemError)
