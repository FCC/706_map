readme.md
=========

706_maps - map for the 706 report
=======


Fixed Map
=========

The fixed map is a 6 color categorical map showing places with at least a certain access stratified by rural or urban classification.  The color scheme is based on a lookup value for available at the benchmark or not in rural or urban (4 classes), is unpopulated, or is water.  A final dataset showing tribal areas is outlined.

The classes attribute structure is a field called myvalue with these codes:

1. fixed availability at 3/768
2. unavailable at 3/768 w/ population
3. unpopulated
4. water

plus a field called rural_urban with these codes:
- U is urban
- R is rural


Data Dependency's
-----------------
Main Data
---------
- tribal lines - PG Layer - `(select * from carto.tribal) as tirbal_lines`
- main706_cty_poly - (Mouseover layer) PG Layer -  `(select gid, geom, cty, cty_name, state_name, fips, to_char(pop_2012,'999,999,999') as pop_2012, round(density,0) as density, to_char(percapinc,'999,999,999') as percapinc `
  `from carto.county, sbi2012june.main706_cty `
  `where county.cty=main706_cty.fips) as main706_cty_poly`
- main706_fixed_poly - PG Layer - `(select * from sbi2012june.main706_fixed_poly) as main706_fixed_poly`
- county_lines - PG Layer - `(select * from carto.county) as county_lines`
- nearshore - PG - Layer - `(select * from carto.water_poly) as nearshore`
- state_high_res - PG Layer - `(select * from carto.state) as state_high_res`

Labels
------
statecentroids - https://raw.github.com/where-gov/fcc/master/basemap/state_centroids.geojson
city-name - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-populated-places-simple.zip

Base
----
- countries - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-admin-0-countries.zip
- islands - PG Layer - (select * from carto.state where state in ('60','66','69','72','78') ) as islands
- country-border - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-admin-0-boundary-lines-land.zip
- state-line - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-admin-1-states-provinces-lines-shp.zip
- coastline - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/physical/10m-coastline.zip
- lake - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/physical/10m-lakes.zip
- land - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/physical/10m-land.zip


Creating the Data
-----------------
tribal - see https://github.com/fccdata/tribal_layer
main706_cty_poly - source county demographics file see - https://raw.github.com/feomike/706_map/master/data/county_demographics_2013.txt is joined to a county layer 
county layer - no url/i right now
main706_fixed_poly - https://github.com/feomike/706_map/blob/master/processing/create_706_fixed_poly.py
water - https://raw.github.com/where-gov/fcc/master/basemap/processing/create_water.py 
state - 
  


Mobile Map
=========

Data Dependency's
-----------------
Main Data
---------
Make sure the wireless at the benchmark is placed on top of the wireless less than the benchmark because they will occupy similar space.

wireless_3_768 - PG Layer - (select * from sbi2012june.shp_wireless
where maxaddown in ('5','6','7','8','9','10') and maxadup in ('3','4','5','6','7','8','9','10') ) as wireless
wireless_lt_3_768 - PG Layer - (select * from sbi2012june.shp_wireless
where maxaddown in ('3','4') and maxadup in ('2') ) as wireless
county_lines - PG Layer - (select * from carto.county) as county_lines
nearshore - PG - Layer - (select * from carto.water_poly) as nearshore
state_high_res - PG Layer - (select * from carto.state) as state_high_res


Labels
------
statecentroids - https://raw.github.com/where-gov/fcc/master/basemap/state_centroids.geojson
city-name - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-populated-places-simple.zip

Base
----
- countries - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-admin-0-countries.zip
- islands - PG Layer - (select * from carto.state where state in ('60','66','69','72','78') ) as islands
- country-border - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-admin-0-boundary-lines-land.zip
- state-line - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/cultural/10m-admin-1-states-provinces-lines-shp.zip
- coastline - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/physical/10m-coastline.zip
- lake - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/physical/10m-lakes.zip
- land - http://mapbox-geodata.s3.amazonaws.com/natural-earth-1.3.0/physical/10m-land.zip

Creating the Data
-----------------
tribal - see https://github.com/fccdata/tribal_layer
main706_cty_poly - source county demographics file see - https://raw.github.com/feomike/706_map/master/data/county_demographics_2013.txt is joined to a county layer 
county layer - no url/i right now
main706_fixed_poly - https://github.com/feomike/706_map/blob/master/processing/create_706_fixed_poly.py
water - https://raw.github.com/where-gov/fcc/master/basemap/processing/create_water.py 
state - 
