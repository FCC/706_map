data
====

This directory holds the data scripts.

- the block_poly_ov_setup.py script sets up the overlay of mosaik data with census blocks.  the resulting data is not used in the map, but in the report.  this script works in PostGIS.  The data ensures that there is one row per (mkg_name, entity, protocol) in the input mosaik data, and that all rows have valid geometry.
- the block_poly_ov.py script actually performs the mosaik block overlay.
