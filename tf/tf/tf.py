# -*- coding: utf-8 -*-
 
data = {'苹果园': (116.177388, 39.927325), '古城': (116.190337, 39.90745)}
import math
def distance_of_stations(point1, point2):
    long1, lat1 = point1
    long2, lat2 = point2
    delta_long = math.radians(long2 - long1)
    delta_lat  = math.radians(lat2 - lat1)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(delta_lat / 2), 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.pow(math.sin(delta_long / 2), 2)))
    s = s * 6378.2
    
    return s
sn = distance_of_stations((113.33573,23.171615),(113.33582,23.171615))
print(sn)