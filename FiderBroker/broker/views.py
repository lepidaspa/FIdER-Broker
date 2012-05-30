from django.http import HttpResponse
from ..broker.models import Proxy

from django.conf import settings
try:
    import json
except:
    import simplejson as json
import urllib2

# Create your views here.
def jsonp_forward(request):
    bb = request.REQUEST.get('BB', [-180,-90,180,90])
    cb = request.REQUEST.get('callback', "get_map")
    #get proxies for bb
    
    proxies = Proxy.geo.get_for_BB(bb)
    
    full_map = []
    #get data from proxy
    for proxy in proxies:    
        full_map.append(proxy.token) 
    ret = ";".join(["%s(%s)" % (cb,tok,) for tok in full_map])
    return HttpResponse(ret)


def get_map(request, proxy):
    proxy = Proxy.objects.get(token = proxy)
    #/data/proxy.token
    return HttpResponse(json.dumps(json.loads(urllib2.urlopen("%s/data/%s" % (settings.FIdER_BROKER, proxy.token,)))))
    