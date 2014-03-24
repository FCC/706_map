#	mike byrne
#	dec. 2, 2013
#	block_poly_ov_setup.py - set up the overlay a poly layer w/ blocks
#	to get the percent area overlay for each block in the output
#	

#- pre processing
#	- import shape file
#	- ensure 1 row per provider
#	- ensure no geometry errors

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
schema = "analysis"
infile = "mosaik_201301_4g"
srcdir = "/users/feomike/documents/analysis/2013/mosaic_overlay_jan2013/Mosaik_January_2013_LTE_HSPAPLUS_WIMAX/"

def importFile(mySHP, myFile):
	mySQL = "DROP TABLE if exists " + schema + "." + myFile + "; commit; "
	cur.execute(mySQL)
	mySQL = "shp2pgsql -s 4326 -I -W latin1 -g geom " + mySHP + " " +  schema + "."
	mySQL = mySQL + myFile + " " +  db + " | psql -p 54321 -h localhost " + db
	os.system(mySQL)
	return()
	
def mkValid(myFile):
	#if any rows have geometry errors, then you need to fix them
	#this part takes a while
	mySQL = "SET enable_seqscan TO off; "
	mySQL = mySQL + "UPDATE " + schema + "." + myFile + " set geom = ST_MakeValid("
	mySQL = mySQL + "geom) where ST_IsValid(geom) = 'f';" 
	mySQL = mySQL + "SET enable_seqscan TO on; "
	mySQL = mySQL + "COMMIT; "
	print "     making geometries valid ..."
#	cur.execute(mySQL)
	return()
	
def mkUnion(myFile):
	#create dissolve 
	mySQL = "SET enable_seqscan TO off; "
	mySQL = mySQL + "DROP TABLE if exists " + schema + "." + myFile + "_union; "
	mySQL = mySQL + "CREATE TABLE " + schema + "." + myFile + "_union as select "
	mySQL = mySQL + "mkg_name, entity, protocol, st_union(geom) as geom from " 
	mySQL = mySQL + schema + "." + myFile + " "
	mySQL = mySQL + "GROUP BY mkg_name, entity, protocol; "
	mySQL = mySQL + "SET enable_seqscan TO on; "
	mySQL = mySQL + "COMMIT; "	
	print "     dissolving geometries ..."
	print mySQL
	cur.execute(mySQL)
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myFile + "_union add COLUMN "
	mySQL = mySQL + " GID SERIAL NOT NULL; "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myFile + "_union add CONSTRAINT "
	mySQL = mySQL + schema + "_" + myFile + "_union_gid_pkey PRIMARY KEY (gid ); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myFile + "_union add CONSTRAINT "
	mySQL = mySQL + " enforce_dims_geom CHECK (st_ndims(geom) = 2); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myFile + "_union add CONSTRAINT "
	mySQL = mySQL + " enforce_srid_geom CHECK (st_srid(geom) = 4326); "
	mySQL = mySQL + "ALTER TABLE " + schema + "." + myFile + "_union add CONSTRAINT "
	mySQL = mySQL + " enforce_geotype_geom CHECK (geometrytype(geom) = 'MULTIPOLYGON'::text "
	mySQL = mySQL + " OR CHECK (geometrytype(geom) = 'POLYGON'::text OR geom IS NULL); "		
	mySQL = mySQL + "CREATE INDEX " + schema + "_" + myFile + "_union_geom_gist ON "
	mySQL = mySQL + schema + "." + myFile + " USING gist (geom); COMMIT; "
	cur.execute(mySQL)	
	return()


#create the connection string to postgres
myConn = "dbname=" + db + " host=" + myHost + " port=" + myPort + " user=" + myUser
conn = psycopg2.connect(myConn)
cur = conn.cursor()

try:
	importFile (srcdir + infile + ".shp", infile)
	mkValid (infile)
	mkUnion (infile)
	
except:
	print "			something bad happened ..."

conn.commit()
cur.close
now = time.localtime(time.time())
print "    end   time:", time.asctime(now)
