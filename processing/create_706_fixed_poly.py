## ---------------------------------------------------------------------------
###   VERSION 0.1 (for postgis)
### create_706_fixed_poly.py
### Created on: June 2, 20123
### Created by: Michael Byrne
### Federal Communications Commission 
##
## ---------------------------------------------------------------------------
##this script creates the fixed polygons for the 706 report
##process is 6 categories
## - rural/populated w/ access at a speed
## - rural/populated w/o access at a speed
## - non-rural/populated w/ access at a speed
## - non-rural/populated w/o access at a speed
## - unpopulated
## - water

#--this script creates the polygon data for the 706 maps
#--these are 4 color polygons of
#--  (1) fixed availability at 3/768
#--  (2) unavailable at 3/768 w/ population
#--  (3) unpopulated
#--  (4) water

##dependencies
##software
##runs in python
##postgres/gis (open geo suite)
##the psycopg library
##data

# Import system modules
import sys, string, os
import psycopg2
import time
now = time.localtime(time.time())
print "local time:", time.asctime(now)

#variables
myHost = "localhost"
myPort = "54321"
myUser = "postgres"
db = "feomike"
schema = "sbi2012june"
oTbl = "main706_fixed_poly"
census_s = "census2010"
benchF = "fixed_3000_768_pop"
  

def create_end_table():
	myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
	conn = psycopg2.connect(myConn)
	myCur = conn.cursor()
	theSQL = "DROP TABLE IF EXISTS " + schema + "." + oTbl + "; "
	theSQL = theSQL + "CREATE TABLE " + schema + "." + oTbl + " as "
	theSQL = theSQL + "SELECT geom, statefp10 as state_fips from " + census_s + ".block_10;"
	theSQL = theSQL + " TRUNCATE " + schema + "." + oTbl + "; ALTER TABLE " + schema + "."
	theSQL = theSQL + oTbl + " add column myvalue character varying(2), "
	theSQL = theSQL + "add column rural_urban character varying(1), "
	theSQL = theSQL + "add column gid serial not null, "
	theSQL = theSQL + "add constraint " + schema + "_" + oTbl + "_pkey PRIMARY KEY (gid), "
	theSQL = theSQL + "add CONSTRAINT " + schema + "_" + oTbl + "_ndims CHECK (st_ndims(geom) = 2), "
	theSQL = theSQL + "add CONSTRAINT " + schema + "_" + oTbl + "_srid_geom CHECK (st_srid(geom) = 900913), "
	theSQL = theSQL + "set with oids;" 
	myCur.execute(theSQL)
	theSQL = "CREATE INDEX " + schema + "_" + oTbl + "_geom_gist ON " + schema + "." 
	theSQL = theSQL + oTbl + "  USING gist (geom); "
	myCur.execute(theSQL)
	myCur.close()
	del myCur, conn, myConn
	return ()

def insert_state_dissolved_polys(myST):
	myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
	conn = psycopg2.connect(myConn)
	myCur = conn.cursor()
	#set up working table
	theSQL = "DROP TABLE IF EXISTS " + schema + ".working; "
	theSQL = theSQL + "CREATE TABLE " + schema + ".working as SELECT gid, "
	theSQL = theSQL + "st_transform(geom,900913) as geom, geoid10, statefp10, water FROM "
	theSQL = theSQL + census_s + ".block_" + myST + "; " 
	theSQL = theSQL + "ALTER TABLE " + schema + ".working add column myvalue smallint, "
	theSQL = theSQL + " add column rural_urban character varying(1), " 
	theSQL = theSQL + " add CONSTRAINT " + schema + "_working_srid_geom CHECK (st_srid(geom) = 900913);"
#	print theSQL
	myCur.execute(theSQL)
	#update column for rural_urban flag	
	theSQL = "UPDATE " + schema + ".working set rural_urban = main706.urban_rural "
	theSQL = theSQL + "from " + schema + ".main706 where geoid10 = main706.block_fips "
	theSQL = theSQL + "and statefp10 = '" + myST + "'; commit;" 
#	print theSQL
	myCur.execute(theSQL)
	#update flag for has at least benchmarck
	theSQL = "UPDATE " + schema + ".working set myvalue = 1 where geoid10 in ("
	theSQL = theSQL + "select block_fips from " + schema + ".main706 where state_fips = "
	theSQL = theSQL + "'" + myST + "' and " + benchF + " > 0); commit;"
#	print theSQL
	myCur.execute(theSQL)
	#update flag for populated and not at benchmarck
	theSQL = "UPDATE " + schema + ".working set myvalue = 2 where myvalue is null and "
	theSQL = theSQL + "  geoid10 in (select block_fips from " + schema + ".main706 where "
	theSQL = theSQL + " pop_2011 > 0 and state_fips = '" + myST + "'); commit; "
#	print theSQL
	myCur.execute(theSQL)
	#update flag for unpopulated 
	theSQL = "UPDATE " + schema + ".working set myvalue = 3 where geoid10 in (select  "
	theSQL = theSQL + "block_fips from " + schema + ".main706 where pop_2011 = 0 and " 
	theSQL = theSQL + "state_fips = '" + myST + "'); commit;"
#	print theSQL
	myCur.execute(theSQL)
	#update flag for water
	theSQL = "UPDATE " + schema + ".working set myvalue = 4 where water = 1; commit;"
#	print theSQL
	myCur.execute(theSQL)
	#perform dissolve
	theSQL = "INSERT INTO " + schema + "." + oTbl + " select st_simplify(st_union(geom), "
	theSQL = theSQL + "5), statefp10 as state_fips, myvalue, rural_urban from "
	theSQL = theSQL + schema + ".working group by state_fips, myvalue, rural_urban; "
	theSQL = theSQL + "commit;"
#	print theSQL
	myCur.execute(theSQL)
	myCur.close()
	del myCur, conn, myConn
	return ()


try:
	#set up the connection to the database
	myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
	conn = psycopg2.connect(myConn)
	theCur = conn.cursor()
	States = ["01","02","04","05","06","08","09"] 
	States = States + ["10","11","12","13","15","16","17","18","19"]
	States = States + ["20","21","22","23","24","25","26","27","28","29"]
	States = States + ["30","31","32","33","34","35","36","37","38","39"]
	States = States + ["40","41","42","44","45","46","47","48","49"]
	States = States + ["50","51","53","54","55","56"]	
	States = States + ["60","66","69","72","78"]
	create_end_table()	
	for theST in States:
		print "going to operate on this state: " + theST
		insert_state_dissolved_polys(theST)
	now = time.localtime(time.time())
	print "local time:", time.asctime(now)
except:
	print "something bad bad happened"     
	
	
	
	
	
	
	



