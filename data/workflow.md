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





