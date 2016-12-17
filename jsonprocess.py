# -*- coding:utf-8 -*-
# #http://blog.csdn.net/theonegis/article/details/50767794
import json
from osgeo import ogr

wkt1 = "POLYGON((0 0,1 0,1 1,0 1,0 0))"
wkt2 = "POLYGON((0 1,1 1,1 2,0 2,0 1))"
poly1 = ogr.CreateGeometryFromWkt(wkt1)
poly2 = ogr.CreateGeometryFromWkt(wkt2)

ring1 = ogr.Geometry(ogr.wkbLinearRing)
ring1.AddPoint(0,0)
ring1.AddPoint(1,0)
ring1.AddPoint(1,1)
ring1.AddPoint(0,1)
ring1.AddPoint(0,0)
ring1.CloseRings()
polygon1=ogr.Geometry(ogr.wkbPolygon)
polygon1.AddGeometry(ring1)

ring2 = ogr.Geometry(ogr.wkbLinearRing)
ring2.AddPoint(0,1)
ring2.AddPoint(1,1)
ring2.AddPoint(1,2)
ring2.AddPoint(0,2)
ring2.AddPoint(0,1)
ring2.CloseRings()
polygon2=ogr.Geometry(ogr.wkbPolygon)
polygon2.AddGeometry(ring2)
union1 = polygon1.Union(polygon2)
#print ring1
#print ring2
#print "union1"
#print union1.ExportToJson()

union = poly1.Union(poly2)

#print poly1
#print poly2
#print "union2"
#print union.ExportToJson()

chinesepath= 'D:/小论文/等值线/2_提取等值线/等值线_3.txt'
uipath = unicode(chinesepath,"utf8")
f = open(uipath,"r")
lines = f.readlines()#读取全部内容
chinesepath1= 'D:/小论文/等值线/2_提取等值线/坐标串_3.txt'
uipath1 = unicode(chinesepath1,"utf8")
file_object = open(uipath1, 'w')

for line in lines:
	list=[]
	#print line
	line_s=json.loads(line);
	#print line_s
	#print line_s.keys()
	#print line_s["49756"]["southwest"]
	keys=line_s.keys()
	for key in keys:
		#print key
		southwest=line_s[key]["southwest"]
		southeast=line_s[key]["southeast"]
		northeast=line_s[key]["northeast"]
		northwest=line_s[key]["northwest"]
		#print southeast[0]
		#print southeast[1]
		wkt = 'POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))' % (southeast[0],southeast[1],northeast[0],northeast[1],northwest[0],northwest[1],southwest[0],southwest[1],southeast[0],southeast[1])
		poly = ogr.CreateGeometryFromWkt(wkt)
		list.append(poly)
	length=len(list)
	for m in range(length):
		if (m>0):
			un = list[m].Union(un)
		elif (m==0):
			un=list[0]
		#print un.ExportToJson()
	file_object.write(un.ExportToJson()+"\n")
file_object.close( )

















