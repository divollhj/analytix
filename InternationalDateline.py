# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:07:44 2019

@author: Jordan
"""
import numpy as np
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import split
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from pyproj import Geod

geod = Geod(ellps='WGS84')


def orderPolygons(xs,ys):
    xs = np.array(xs)
    ys = np.array(ys)
    
    center = np.average(xs),np.average(ys)
    points = zip(xs,ys)
    points.sort(key=lambda p: np.arctan2(p[1]-center[1],p[0]-center[0]))
    array = np.array(points)
    return array[:,0],array[:,1]

def circleLatLons(lat, lon, radiuskm,n_samples=180):
    """
    Return the coordinates of a geodetic circle of a given
    radius about a lon/lat point.

    Radius is in meters in the geodetic's coordinate system.

    """
    radius = radiuskm * 1000.
    lons, lats, back_azim = geod.fwd(np.repeat(lon, n_samples),
                                     np.repeat(lat, n_samples),
                                     np.linspace(360, 0, n_samples),
                                     np.repeat(radius, n_samples),
                                     radians=False,
                                     )
    return lats, lons

def ellipseLatLons(lat,lon,major,minor,orientation,n_samples=180,units='km'):
    """
    Return the coordinates of a geodetic circle of a given
    radius about a lon/lat point.

    Radius is in meters in the geodetic's coordinate system.

    """
    if units == 'km':
        major = major*1000.
        minor = minor*1000.
    orientation = np.deg2rad(orientation)
    bearing = np.linspace(2*np.pi,0,n_samples)
    radius = np.true_divide(np.multiply(major,minor),np.sqrt(np.square(np.multiply(major,np.sin(bearing+orientation))) + np.square(np.multiply(minor,np.cos(bearing+orientation)))))

    lons, lats, back_azim = geod.fwd(np.repeat(lon, n_samples),
                                     np.repeat(lat, n_samples),
                                     np.linspace(360, 0, n_samples),
                                     radius,
                                     radians=False,
                                     )
    return lats,lons

def latlonCircleRadiusKM(lat, lon, radiusKM):
    '''
    lat, lon are the center of the circle, radiusKM is the radius in Km of the circle
    This will return a list of lat lon points that define a circle, for speed sake the number of points is 180 1 every 2 degrees
    This also takes into account projection effects with the Earth, so the closer to the north pole, the more oval
    shape the circle will become.
    '''
    #earth radius in km
    R = 6378.1
    distanceKM = radiusKM/R
    latArray = []
    lonArray = []
    lat = np.deg2rad(lat)
#    lat = np.deg2rad(90.)
    lon = np.deg2rad(lon)
    brng = np.linspace(0,2*np.pi,180)
    lat2 = np.arcsin(np.sin(lat) * np.cos(distanceKM) 
            + np.cos(lat) * np.sin(distanceKM) * np.cos(brng))

    lon2 = lon + np.arctan2(np.sin(brng)*np.sin(distanceKM)
            * np.cos(lat),np.cos(distanceKM)-np.sin(lat)*np.sin(lat))

    lon2 = np.rad2deg(lon2)
    lat2 = np.rad2deg(lat2)
    latArray = list(lat2)
    lonArray = list(lon2)

    return latArray,lonArray


def handle_InternationalDateline(iLat,iLon):
    '''
    iLat and iLon must be iterables
    if there are no points that lie around the ID then I'll return the originals in a list [[lats]],[[lons]] that make a closed polygon
    if there are points that lie around the ID then I'll return a list of lists of separated points with new points on the dateline
    [[lats on left][lats on right]],[[lons on left],[[lons on right]]
    This keeps the output consistent no matter what happens in the function
    '''
    #Just convert to numpy arrays off the wiffle ball bat
    nlats = np.array(list(iLat))
    nlons = np.array(list(iLon))
    
    #Correct the points
    nlons = np.where(nlons >= 0 ,nlons,nlons+360)
    nlons = np.where(nlons <= 360,nlons,nlons-360)
    #Return the points
    nlons = np.where(nlons <= 180,nlons,nlons-360)
    rlats,rlons = [],[]
    if max(nlons)-min(nlons) > 300:
        posidx = nlons > 0
        negidx = nlons < 0
        poslons = nlons[posidx]
        poslats = nlats[posidx]
        neglons = nlons[negidx]
        neglats = nlats[negidx]
        if posidx.any():
            poslons -= 180
        if negidx.any():
            neglons += 180
        alllons = np.append(poslons,neglons)
        alllats = np.append(poslats,neglats)
        alllons,alllats = orderPolygon(alllons,alllats)
        plt.scatter(alllons,alllats)
        poly = Polygon(zip(alllons,alllats))
        line = LineString([(0,-5000),(0,5000)])
        spoly = split(poly,line)
        for polygon in spoly:
            xx,yy = np.array(polygon.exterior.xy[0]),np.array(polygon.exterior.xy[1])
            posidx = xx > 0
            negidx = xx < 0
            if posidx.any():
                xx += -180
            if negidx.any():
                xx -= -180
            rlats.append(yy)
            rlons.append(xx)
        return rlats,rlons
    else:
        nlons,nlats = orderPolygon(nlons,nlats)
        polygon = Polygon(zip(nlons,nlats))
        xx,yy = np.array(polygon.exterior.xy[0]),np.array(polygon.exterior.xy[1])
        rlats.append(yy)
        rlons.append(xx)
        return rlats,rlons

    
if __name__ == '__main__':
    #Some Crazy shape from silly numbers
#    lats = np.array([0,1,2,3,4])
#    lons = np.array([189.0,-179,160,165,180])
    #Circle that doesn't cross the ID
#    lons,lats = Point(130,88).buffer(30).exterior.xy
    #Circle that crosses the ID
#    lons,lats = Point(130,90).buffer(20).exterior.xy
    #Rectangle that spans the ID
#    lats = [-40,40,-40,40]
#    lons = [-160,150,160,-150]
    
    #Circle made with stuff
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
#    lats,lons = circleLatLons(80,-180,50)
    
#    lats, lons = circleLatLons(87,0,500,50000)
#    lats,lons = ellipseLatLons(0,12,31,20,3.0368)

    y,x = handle_InternationalDateline(lats,lons)
    for x,y in zip(x,y):
        plt.plot(x,y)
    plt.gca().set_aspect('equal')
    plt.show()