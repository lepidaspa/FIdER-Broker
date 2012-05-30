from django.db import models
from django.db.models import Q
# Create your models here.


class GeoManager(models.Manager):
    def get_for_BB(self, BB):
        fullworld = [-180, -90, 180, 90]
        if BB == fullworld:
            return Proxy.objects.all()
        
        w = BB[0]
        s = BB[1]
        e = BB[2]
        n = BB[3]
        
        #BB_east > BB_west
        #BB_north > BB_south
        
        q_in = Q()  
        
        se_in = Q(Q(BB_west<e), Q(BB_east>e), Q(BB_south<s), Q(BB_north>s))
        
        ne_in = Q(Q(BB_west<e), Q(BB_east>e), Q(BB_south<n), Q(BB_north>n))
        
        sw_in = Q(Q(BB_west<w), Q(BB_east>w), Q(BB_south<s), Q(BB_north>s))
        
        nw_in = Q(Q(BB_west<w), Q(BB_east>w), Q(BB_south<n), Q(BB_north>n))
        
        q_in.add(se_in, Q.OR)
        q_in.add(ne_in, Q.OR)
        q_in.add(nw_in, Q.OR)
        q_in.add(sw_in, Q.OR)
        
        
        return Proxy.objects.filter(q_in)

class Proxy(models.Model):
    url = models.URLField()
    manifest = models.TextField(null=True, blank=True)
    token = models.TextField(unique=True)
    mode = models.TextField()
    BB_north = models.FloatField()
    BB_east = models.FloatField()
    BB_south = models.FloatField()
    BB_west = models.FloatField()
    
    geo = GeoManager()
        
    
     
    
    
class Metadata(models.Model):
    proxy = models.ForeignKey(Proxy)
    meta = models.TextField()
    
