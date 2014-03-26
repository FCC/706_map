workflow.md
===========

The Section 706 Workflow Description
------------------------------------

This document describes the workflow for the 706 data analysis and mapping projects.  The primary steps are:
- Step 1: Prepare 706 Table
- Step 2: Prepare Mosaik percent overlap tables
- Step 3: Prepare Maps


Step 1: Prepare 706 Table
-------------------------
The 706 table (e.g. main706) is the primary analysis used for the 706 report.  It is generated from the National Broadband Map contractor team (computech at the initial writing of this document), and contains 1 record per block, with a set of metrics of population/housing units in each block which have fixed broadband at a certain speed available to it.  Below is an example of what this table looks like:

<table>
    <tr><td>Column</td><td>Definition</td></tr>
    <tr><td>block_fips</td><td>15 character block code </td></tr>
    <tr><td>pop_2011</td><td>population for the year 2011 in that block</td></tr>
    <tr><td>hhu_2001</td><td>housing units fof 2011 in that block</td></tr>
    <tr><td>state_fips</td><td>2 character code for the State fips containing the block</td></tr>
    <tr><td>state_name</td><td>State Name containing the block</td></tr>
    <tr><td>county_fips</td><td>5 character code for the state+county containg the block</td></tr>
    <tr><td>county_name</td><td>County name containing the block</td></tr>
    <tr><td>cdist_id</td><td>7 character code for the congressional district containing the block</td></tr>
    <tr><td>urban_rural</td><td>1 character flag for the block being urban or rural</td></tr>
    <tr><td>fixed_768_200_pop</td><td>Population in the block with access to fixed broadband of at least 768 down and 200 up</td></tr>
    <tr><td>fixed_768_200_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 768 down and 200 up</td></tr>
    <tr><td>fixed_3000_768_pop</td><td>Population in the block with access to fixed broadband of at least 3 Mbps down and 768 up</td></tr>
    <tr><td>fixed_3000_768_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 3 Mbps down and 768 up</td></tr>
    <tr><td>fixed_6000_15000_pop</td><td>Population in the block with access to fixed broadband of at least 6 Mbps down and 1.5 Mbps up</td></tr>
    <tr><td>fixed_6000_15000_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 6 Mbps down and 1.5 Mbps up</td></tr>
    <tr><td>fixed_10000_768_pop</td><td>Population in the block with access to fixed broadband of at least 10 Mbps down and 768 up</td></tr>
    <tr><td>fixed_10000_768_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 10 Mbps down and 768 up</td></tr>
    <tr><td>fixed_10000_1500_pop</td><td>Population in the block with access to fixed broadband of at least 10 Mbps down and 1.5 Mbps up</td></tr>
    <tr><td>fixed_10000_1500_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 10 Mbps down and 1.5 Mbps up</td></tr>    
    <tr><td>fixed_10000_3000_pop</td><td>Population in the block with access to fixed broadband of at least 10 Mbps down and 3 Mbps up</td></tr> 
    <tr><td>fixed_10000_3000_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 10 Mbps down and 3 Mbps up</td></tr>
    <tr><td>fixed_10000_6000_pop</td><td>Population in the block with access to fixed broadband of at least 10 Mbps down and 6 Mbps up</td></tr>
    <tr><td>fixed_10000_6000_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 10 Mbps down and 6 Mbps up</td></tr>
    <tr><td>fixed_25000_3000_pop</td><td>Population in the block with access to fixed broadband of at least 25 Mbps down and 3 Mbps up</td></tr>
    <tr><td>fixed_25000_3000_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 25 Mbps down and 3 Mbps up</td></tr>
    <tr><td>fixed_25000_10000_pop</td><td>Population in the block with access to fixed broadband of at least 25 Mbps down and 10 Mbps up</td></tr>
    <tr><td>fixed_25000_10000_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 25 Mbps down and 10 Mbps up</td></tr>
    <tr><td>fixed_100000_50000_pop</td><td>Population in the block with access to fixed broadband of at least 100 Mbps down and 50 Mbps up</td></tr>
    <tr><td>fixed_100000_50000_hhu</td><td>Housing Units in the block with access to fixed broadband of at least 100 Mbps down and 50 Mbps up</td></tr>
</table>

Fixed technology includes, DSL, Copper, Cable, Fiber, Fixed Wireless, Other and BPL.  Fields then repeat for the same speed teirs in mobile technology.  

Step 2: Prepare Mosaik percent overlap tables
---------------------------------------------
This phase of the project takes the 3G and 4G polygons from Mosaik, and overlays them with Census Blocks.  The final output here is a collection of blocks with the maximum percent overlap from ANY Mosaik 3G or 4G service.  The resulting table is one row per block with the maximum percent overlap; the provider and specific technology is not applied.  The 706 team uses this in conjunction w/ the centroid method acquired from the WTB.  This process will change when we use new form 477 rather than Mosaik as the primary collection.  The processing here has 3 parts;
- Part 1 - Pre-procesisng steps
- Part 2 - Overlay with blocks by state
- Part 3 - Combine resulting state tables and acquire maximum percent overlay per block

**_Step 2: Part 1 - Pre-procesisng steps_**
This step in the process primarily takes the input Mosaik Shape files and ensures, (a) there are no geometry errors, (b) and there is one row per provider/technology combination.  Doing this makes the process exactly like the NBM wireless overlay processing.  In general, the Mosaik data seems to come in with a significant number of geometry issues.

I have written [code to perform this step in python/PostGIS](https://github.com/fccdata/706_map/blob/master/processing/block_poly_ov_setup.py) for doing this.  I have found that this code takes a super long time, becuase (a) the Mosaik data has so many geometry errors, (b) PostGIS processing here is slow, unless the DB is tuned appropriately, and (c) generally ArcGIS dissolves are faster.  I have switched to procesisng these steps by hand in ArcGIS desktop rather than PostGIS.  **_sigh_**.  

The result here should be a single shapefile (or could be single feature class in a file geodatabase) which has (a) no geometry errors and (b) 1 row per mkg_name, entity, protocol (e.g. provider name and technology).

**_Step 2: Part 2 - Overlay with blocks by state_**
I have found that processing this in ArcGIS desktop is smoother and faster generally.  I imagine w/ time one could optimize the PostGIS setup to handle these this faster, I just haven't had the time to do so.  I have written both a [PostGIS](https://github.com/fccdata/706_map/blob/master/processing/block_poly_ov.py) and an [ArcGIS](https://github.com/fccdata/706_map/blob/master/processing/mosaic_block_overlay_esri.py) approach to procesisng the Mosaik / Block overlay.  I reccommend using the [ArcGIS](https://github.com/fccdata/706_map/blob/master/processing/mosaic_block_overlay_esri.py).

The ArcGIS script runs in a set of loops.  For each state, it runs for all OBjectID's in the Mosaik Feature Class.  One could change up the ID line to it only performed on a certain set (above, below, equal to) of ObjectIDs.

The results from this script are a set of tables inside the processing file geodatabase with the percent of overlap from each block for each single feature in the Mosaik input feature.  

**_Step 2: Part 3 - Combine resulting state tables_**
The goal is to acquire the maximum overlap of 3G/4G for each block.  Since the result of Step 2: Part 2 completes, is a set of tables, we (a) aggreate these tables to single tables, (b) export these state tables to csv, (c) import these state csv's to 1 single Postgres table, and (d) export to one csv for the 706 team one row per block w/ the maximum percent overlap.

In order to aggreate the individual file geodatabase state / Mosaik features tables to state tables, run the following [python/ArcGIS script](https://github.com/fccdata/706_map/blob/master/processing/Mosaic_Wireless_Block_Append.py).  This script will need to be edited to make sure the source fgdbs are appropriately being pointed to.  The results of this script are one table per state in a single FGDB.

In order to export the resulting state only tables to csv, run the following [python/ArcGIS script](https://github.com/fccdata/706_map/blob/master/processing/Mosaic_Wireless_Block_Append.py).  This script will beed to be edited to make sure the source fgdbs are appropriately being pointed to.  The results of this script are 1 csv per state table.

Import the csv's into PostGres with the following [python/psycopg script]().  This script will need to be edited to make sure the source csv's and results tables are appropriately being pointed to.  The results of this script are 1 table in PostGres with rows for each of the imported state csv's.

The final step here is to export the data as a csv for the 706 team which has 1 row per block (e.g. block_fips) and the maximum percent overlap of that block with any 3G/4G service.  To do this use this [python/psycopg script]().  This script will need to be edited to make sure the appropriate source data is being pointed to.  The results is one csv to be handed to the 706 data team.

Step 3: Prepare Maps
-------------------------



