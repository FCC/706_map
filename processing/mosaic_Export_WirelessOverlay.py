# ---------------------------------------------------------------------------
# mosaic_Export_WirelessOverlay.py
# Created on: May 24, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# exports the feature classes for the block table
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math

#global variables
theOF = "C:/Users/michael.byrne/analysis/2014/mosaik/"
theFGDB = "C:/Users/michael.byrne/analysis/2014/mosaik/processing_lte.gdb/"
theSuffix = "_Mosaic-WirelessOverlay.csv"
thePrefix = "wireless_block_"

States = ["AK","AL","AR","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3
States = States + ["MI","MN","MO","MS","MT","NC","ND"] #4
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VT","WA","WI","WV","WY"] #7 


#Function sbdd_ProviderReport writes out the unique Provider Values Detail
#has no argument; 
def sbdd_exportFile (myTbl, myOutFile):
    #go open up and read this table
    myFile = open(myOutFile, 'a')
    arcpy.AddMessage(myTbl)
    for row in arcpy.SearchCursor(myTbl):
        myOID = str(row.getValue("OBJECTID")).strip()
        myBlk = str(row.getValue("GEOID10")).strip()
        myPCT = str(row.getValue("PCT")).strip()
        myName = str(row.getValue("MKG_NAME")).strip()        
        myProv = str(row.getValue("ENTITY").encode('utf-8')).strip()
        myPro = str(row.getValue("PROTOCOL").encode('utf-8')).strip() 
        myStr = myOID + "|" + myBlk + "|" + myPCT + "|"
        myStr = myStr + myName + "|" + myProv + "|" + myPro 
        myFile.write(myStr +  "\n")
        del myOID, myBlk, myPCT
        del myName, myProv, myPro
        del myStr
    myFile.close()
    del row

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:

        theHead = "SHAPEID|CENSUSBLOCK_FIPS|PCT_BLK_IN_SHAPE|NAME|"
        theHead = theHead + "ENTITY|PROTOCOL"
        #write output
        theTbl = theFGDB + thePrefix + theST
        if arcpy.Exists(theTbl):
            outFile = theOF + theST + theSuffix
            myFile = open(outFile, 'w')
            myFile.write(theHead + "\n")
            myFile.close()            
            myCnt = str(arcpy.GetCount_management(theTbl).getOutput(0))
            theMsg = "     going to write out this many records for "
            theMsg = theMsg + theST + ": " + str(myCnt)
            sbdd_exportFile(theTbl, outFile)
            del myFile, outFile, theMsg, myCnt            
        else:
            theMsg = "     wireless overlay table for " + theST
            theMsg = theMsg + " does not exist" 
            arcpy.AddMessage(theMsg)
            del theMsg
    del theHead, theST, States, theTbl, thePrefix
    del theOF, theSuffix
except:
    arcpy.AddMessage("Something bad happened")


  
