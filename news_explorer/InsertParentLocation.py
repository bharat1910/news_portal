__author__ = 'bharat'

from news_explorer.models import Location, ParentLocation

try:
    def insertParentLocation():
        locationToParentMap = {}
        parents = []
        parentsToIdMap = {}

        L = Location.objects.all()
        for l in L:
            if l.name not in locationToParentMap.keys():
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
        return "dummy"
except:
    print(SystemError)
