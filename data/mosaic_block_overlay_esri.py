# ---------------------------------------------------------------------------
# mosaic_block_overlay_esri.py
# Created on: May 16, 2011 
# Created by: Michael Byrne
# Federal Communications Commission
# performs the wireless polygon overlay
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
from arcpy import env
import sys, string, os, math


#write out global variables
theDir = "C:/Users/michael.byrne/analysis/2014/Mosaik/"
thePGDB = theDir + "processing_2.gdb"  #processing file geodatabase
arcpy.env.workspace = thePGDB

theFC = "/mosaik_lte_2013_07"

theBlockGDB = "C:/Users/michael.byrne/Library/TabBlock_2010.gdb/"

States = ["AK","AL","AR","AS","AZ","CA","CO","CT"]          #1
States = States + ["DC","DE","FL","GA","GU","HI","IA","ID"] #2
States = States + ["IL","IN","KS","KY","LA","MA","MD","ME"] #3 
States = States + ["MI","MN","MO","MP","MS","MT","NC","ND"] #4 
States = States + ["NE","NH","NJ","NM","NV","NY","OH","OK"] #5
States = States + ["OR","PA","PR","RI","SC","SD","TN","TX"] #6
States = States + ["UT","VA","VI","VT","WA","WI","WV","WY"] #7

theOutPrj = "PROJCS['North_America_Albers_Equal_Area_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',20.0],PARAMETER['Standard_Parallel_2',60.0],PARAMETER['Latitude_Of_Origin',40.0],UNIT['Meter',1.0]]"
theInPrj = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
theTransform = "NAD_1983_To_WGS_1984_1"


##write out functions
##Function sbdd_ExportToShape exports the created layers to shapefiles in
##appropriate directories
def blockIntersect():
    arcpy.AddMessage("     Begining overlay Processing")
    if arcpy.Exists("wireless_block_" + theST):
        arcpy.Delete_management("wireless_block_" + theST)
    theCnt = int(arcpy.GetCount_management(thePGDB + theFC).getOutput(0))
    theBlock = theBlockGDB + "Block_" + theST
    myID = 1
    while theCnt >= myID:  #if there are records in the wireless shape class
        arcpy.AddMessage("     Performing overlay " + str(myID) + 
                         " of " + str(theCnt) + " and O-ID: " + 
                         str(myID))            
        myQry = "OBJECTID = " + str(myID)
        myLyr = "Mosaic" + theST + str(myID)
        arcpy.MakeFeatureLayer_management (thePGDB + theFC, myLyr, myQry)
        #if there there are records in myLyr, then process
        if int(arcpy.GetCount_management(myLyr).getOutput(0)) > 0:   
            theOFC = "wireless_block_" + theST + "_" + str(myID)
            theOFCP = "wireless_block_" + theST + "_" + str(myID) + "_prj"
            myFCs = [theOFC, theOFCP]
            for myFC in myFCs:
                if arcpy.Exists(myFC):
                    arcpy.Delete_management(myFC)
            blLyr = "block" + theST
            arcpy.MakeFeatureLayer_management (theBlock, blLyr)
            arcpy.SelectLayerByLocation_management (myLyr,"intersect",blLyr,"",
                                                    "NEW_SELECTION")                
            theSelCnt = arcpy.GetCount_management(myLyr).getOutput(0)
            arcpy.Delete_management(blLyr) 
            arcpy.Delete_management(myLyr)
            if int(theSelCnt) > 0:  #there ARE records in the intersect
                arcpy.AddMessage("          performing intersect...")
                #perform the intersection on both feature classes
                arcpy.Intersect_analysis([thePGDB + theFC, theBlock], theOFC)                  
                arcpy.Project_management(theOFC, theOFCP, theOutPrj, 
                                         theTransform, theInPrj)                
                arcpy.AddField_management(theOFCP, "PCT" ,"DOUBLE", 
                                          "5" , "2", "")                
                theExp = "([SHAPE_Area]) /( [ALAND10] + [AWATER10] )*100"                
                arcpy.CalculateField_management(theOFCP, "PCT", 
                                                theExp, "VB", "")
                if arcpy.Exists(theOFC):
                    arcpy.Delete_management(theOFC)
                myQry = "PCT > 100"
                myLyrC = theST + "gtOne" + str(myID)                
                arcpy.MakeFeatureLayer_management (theOFCP, myLyrC, myQry)
                if int(arcpy.GetCount_management(myLyrC).getOutput(0)) > 0:                    
                    arcpy.CalculateField_management(myLyrC, "PCT", "100", 
                                                    "PYTHON", "")                    
                arcpy.Delete_management(myLyrC)                
                arcpy.CopyRows_management(theOFCP, theOFC)
                if arcpy.Exists(theOFCP):
                    arcpy.Delete_management(theOFCP)
                del theExp
                
            del theOFC, theOFCP, myFC, myFCs
        myID = myID + 1    
    del myLyr, myQry, theBlock, theCnt, myID
    return ()

#****************************************************************************
##################Main Code below
#****************************************************************************
try:
    for theST in States:
        arcpy.AddMessage("the state is: " + theST)
        blockIntersect()
        #open a file to write when it finished
        outFile = theDir + "/wireless_overlay_" + theST + ".txt"
        myFile = open(outFile, 'w')
        myFile.write(theST + ": finished\n")
        myFile.close()
    del theST, States
except:
    arcpy.AddMessage("Something bad happened")

