#	mike byrne
#	dec. 2, 2013
#	block_poly_ov.py - overlay a poly layer (mosaik) w/ blocks
#	to get the percent area overlay for each block in the output
#	
#- processing
#	- for each state;
#	- for each mosaik gid
#	- select all block gid's that are 100 percent within a mosaik polygon
#		- write those to a file
#	- for those that touch, but are not 100% within a mosaik polygon, do an overlay; 
#	- get the percent area overlap; write it to a file

import os
import pprint
import string
import psycopg2
import time
import datetime
from datetime import date

now = time.localtime(time.time())
print "    start time:", time.asctime(now)

#global variables - database connection
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
cen_schema = "census2010"
schema = "analysis"
inTab = "test" #"iwireless"
outTB = "mo_ov"

def defineOutput():
	mySQL = "DROP TABLE IF EXISTS " + schema + "." + outTB + "; "
	mySQL = mySQL + "CREATE TABLE " + schema + "." + outTB + " ( "
	mySQL = mySQL + "geoid10 character varying(15), "
	mySQL = mySQL + "mkg_name character varying(75), "
	mySQL = mySQL + "entity character varying(75), "
	mySQL = mySQL + "protocol character varying(75), "
	mySQL = mySQL + "pct_covered numeric ) "
	mySQL = mySQL + " WITH (  OIDS=FALSE ); ALTER TABLE " + schema + "." + outTB
	mySQL = mySQL + " OWNER TO postgres; "
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + outTB + "_geoid10_btree "
	mySQL = mySQL + "ON " + schema + "." + outTB + " USING btree "
	mySQL = mySQL + "(geoid10); "
	cur.execute(mySQL)
	return()

#single geometries are much better for ST_Contains 
#(in fact the documentation says don't use collections)
#step 1: create a table of single geometries
def mkWorking(myGID):
	mySQL = "DROP TABLE IF EXISTS " + schema + ".working; "
	mySQL = mySQL + "CREATE TABLE " + schema + ".working as " 
	mySQL = mySQL + "SELECT (ST_Dump(geom)).geom as geom, "
	mySQL = mySQL + "mkg_name, entity, protocol from "
	mySQL = mySQL + schema + "." + inTab + " WHERE gid = "
	mySQL = mySQL + myGID + "; " 
	mySQL = mySQL + "ALTER TABLE " + schema + ".working ADD COLUMN gid serial not null; "
	cur.execute(mySQL)
	mkGeoTB("working", "gid")
	return()
	
#step 2: get all of those blocks which are wholly contained within the mosaic polygon
#these have a percent of 100 overlap
def getContained(cenTab):
	mySQL = "SET enable_seqscan TO off; "
	mySQL = mySQL + "INSERT INTO " + schema + "." + outTB 
	mySQL = mySQL + " (geoid10, mkg_name, entity, protocol) "	
	mySQL = mySQL + "SELECT geoid10, mkg_name, entity, protocol "
	mySQL = mySQL + "from " + cen_schema + "." + cenTab + ", " + schema + ".working" 
	mySQL = mySQL + " where ST_Contains(working.geom, " + cenTab + ".geom); "
	mySQL = mySQL + "SET enable_seqscan TO on; "
	mySQL = mySQL + "UPDATE " + schema + "." + outTB + " SET pct_covered = 100 "
	mySQL = mySQL + "WHERE pct_covered is NULL; "
	mySQL = mySQL + "COMMIT; "
	cur.execute(mySQL)	
	return()


#step 3: get a table of only those blocks which overlap and are not 
#100 percent within the mosaic
def getNotContained(cenTab):
	mySQL = "DROP TABLE IF EXISTS " + schema + ".not_contained; "
	mySQL = mySQL + "CREATE TABLE " + schema + ".not_contained as "
	mySQL = mySQL + "SELECT " + cenTab + ".geoid10, " + cenTab + ".gid, " + cenTab
	mySQL = mySQL + ".geom, aland10 + awater10 as totarea FROM " + cen_schema + "." + cenTab 
	mySQL = mySQL + " LEFT JOIN " + schema + "." + outTB + " on " + cenTab + ".geoid10="
	mySQL = mySQL + outTB + ".geoid10 WHERE " + outTB + ".geoid10 is NULL; "
	cur.execute(mySQL)
	mkGeoTB("not_contained","gid")
	return()

#step 4: of the intersecting blocks, intersect them 
#using this equal area projection
#http://spatialreference.org/ref/sr-org/44/ 
def getIntersects():
	mySQL = "SET enable_seqscan TO off; "
	mySQL = mySQL + "DROP TABLE IF EXISTS " + schema + ".intersects; "
	mySQL = mySQL + "CREATE TABLE " + schema + ".intersects as "
	mySQL = mySQL + "SELECT st_union(ST_Intersection(working.geom, not_contained.geom)) "
	mySQL = mySQL + "as geom, geoid10, totarea, mkg_name, entity, protocol "
	mySQL = mySQL + "FROM " + schema 
	mySQL = mySQL + ".working, " + schema + ".not_contained WHERE ST_INTERSECTS("
	mySQL = mySQL + "working.geom, not_contained.geom) "
	mySQL = mySQL + "GROUP BY geoid10, totarea, mkg_name, entity, protocol; "
	mySQL = mySQL + "SET enable_seqscan TO on; "
	mySQL = mySQL + "ALTER TABLE " + schema + ".intersects ADD COLUMN gid "  
	mySQL = mySQL + "serial not NULL; "
	cur.execute(mySQL)
	mkGeoTB("intersects", "gid")
	return()

def mkGeoTB(myTB, myPkey):
	mySQL = "ALTER TABLE " + schema + "." + myTB + " ADD CONSTRAINT " + schema 
	mySQL = mySQL + "_" + myTB + "_" + myPkey + "_pkey PRIMARY KEY (" + myPkey + "); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myTB + " ADD CONSTRAINT " 
	mySQL = mySQL + "enforce_dims_geom CHECK (st_ndims(geom) = 2); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myTB + " ADD CONSTRAINT " 
	mySQL = mySQL + "enforce_srid_geom CHECK (st_srid(geom) = 4326); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myTB + " ADD CONSTRAINT " 
	mySQL = mySQL + "enforce_geotype_geom CHECK (geometrytype(geom) = 'POLYGON'::text "
	mySQL = mySQL + "OR geometrytype(geom) = 'MULTIPOLYGON'::text OR "
	mySQL = mySQL + "geometrytype(geom) = 'GEOMETRYCOLLECTION'::text OR "
	mySQL = mySQL + "geom IS NULL); "
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + myTB + "_geom_gist ON " + schema 
	mySQL = mySQL + "." + myTB + " USING gist (geom); "
	cur.execute(mySQL)
	return()	 

def getPctOv():
	mySQL = "SET enable_seqscan TO off; "
	mySQL = mySQL + "INSERT INTO " + schema + "." + outTB 
	mySQL = mySQL + " (geoid10, mkg_name, entity, protocol, pct_covered) "	
	mySQL = mySQL + "SELECT geoid10, mkg_name, entity, protocol, "
	mySQL = mySQL + "(st_area(st_transform(geom, 2163)) / totarea) * 100 "
	mySQL = mySQL + "FROM " + schema + ".intersects; " 
	mySQL = mySQL + "COMMIT; "
	cur.execute(mySQL)	
	return()


#create the connection string to postgres
myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()

try:
	defineOutput()
	States = ["01","02","04","05","06","08","09","10"]          #1
	States = States + ["11","12","13","15","16","17","18","19"] #2
	States = States + ["20","21","22","23","24","25","26","27"] #3 
	States = States + ["28","29","30","31","32","33","34","35"] #4 
	States = States + ["36","37","38","39","40","41","42","44"] #5
	States = States + ["45","46","47","48","49","50","51","53"] #6
	States = States + ["54","55","56","60","66","69","72","78"] #7
	States = ["19"]
	mySQL = "SELECT MAX(gid) from " + schema + "." + inTab + "; "
	cur.execute(mySQL)
	maxgid = cur.fetchone()[0]
	cnt = 0
	while cnt <  maxgid:
		cnt = cnt + 1
		print "     doing polygon: " + str(cnt)
		#get all blocks wholly within the wireless poly
		for theST in States:
			print "          doing state: " + str(theST)
			mkWorking(str(cnt))
			print "               starting contained ..."
			getContained("block_" + str(theST))
			print "               starting not contained ..."
			getNotContained("block_" + str(theST))
			print "               starting intersects ..."
			getIntersects()
			print "               starting pct_ov ..."
			getPctOv()
except:
	print "			something bad happened ..."

conn.commit()
cur.close
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)



