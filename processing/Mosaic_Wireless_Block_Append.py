# ---------------------------------------------------------------------------
# Mosaic_Wireless_Block_Append.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# Appends the results of the Wireless Block overlay into State Tables
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

##Global Variables
#the Output Location is thePGDB 
thePGDB = "C:/Users/michael.byrne/analysis/2014/Mosaik/processing.gdb"  
arcpy.env.workspace = thePGDB

#input file geodatabase is theInFGDB 
theInFGDB = "C:/Users/michael.byrne/analysis/2014/Mosaik/processing_3.gdb" 

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MS","MT","NC","ND","MP"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6 
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7


##write out functions
##Function sbdd_CreateTable defines a new state table into which all state records will be appended
def sbdd_CreateTable(myTbl):
    arcpy.AddMessage("  Creating output table:" + myTbl)
    if arcpy.Exists(myTbl):
        arcpy.Delete_management(myTbl)
    arcpy.CreateTable_management(thePGDB, myTbl)        
    arcpy.AddField_management(myTbl, "GEOID10", "TEXT", "", "", "15")
    arcpy.AddField_management(myTbl, "PCT" ,"DOUBLE", "5" , "2", "")
    arcpy.AddField_management(myTbl, "MKG_NAME", "TEXT", "", "", "100")
    arcpy.AddField_management(myTbl, "ENTITY", "TEXT", "", "", "100")
    arcpy.AddField_management(myTbl, "PROTOCOL", "TEXT", "", "", "20")
    del myTbl
    return ()


##Function sbdd_AppendRecords appends records of each set to the state created table
def sbdd_AppendRecords(myTbl):
    arcpy.AddMessage("     Begining Append Processing")
    #theCnt is a variable which assumes the highest ObjectID of the input Mosaik shapes
    #in this context it is expecting the individual overlay's to be named with this number
    #as a suffix.  it is set at a suitably high enough number to get all the Mosaic/Block
    #overlay tables, BUT YOU SHOULD CHECK FIRST!
    theCnt = int('100')
    myCnt = 1   
    while myCnt <= theCnt:
        inTbl = theInFGDB + "/wireless_block_" + theST + "_" + str(myCnt)
        arcpy.AddMessage(inTbl)
        if arcpy.Exists(inTbl):
            arcpy.AddMessage("     Appending " + str(myCnt) + " of " + str(theCnt))
            arcpy.Append_management([inTbl], myTbl, "NO_TEST")
        myCnt = myCnt + 1
    del myTbl, theCnt, myCnt, inTbl

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        sbdd_CreateTable("wireless_block_" + theST)
        sbdd_AppendRecords("wireless_block_" + theST)
    del theST, States, thePGDB, theInFGDB
except:
    arcpy.AddMessage("Something bad happened")


  
