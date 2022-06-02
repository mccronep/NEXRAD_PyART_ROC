#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#==============================================================
#
#==============================================================
#
#
#==-FNMOC/N38DI PYTHON PROGRAM DEFINITION-==========================================
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# Py_nexrad_image_process.py
# :::::::::::::::::::::::::::::::::::::::::::::::
#
#  PROGRAM OVERVIEW:
#       (0) The PYTHON CODE manages the overall data conversion process. 
#       (1) This code uses PyART from arm.gov to process the NEXRAD imagery. 
#
#--------------------------------------------------------------------------------------------------
# PARAMETER TABLE:
#--------------------------------------------------------------------------------------------------
#
# I/O           NAME                               TYPE            FUNCTION
#--------------------------------------------------------------------------------------------------
#  I            Compressed NEXRAD Level II file    input           INPUT DATA FROM NWS via 557 WW [AFWA]
#  O            JPG/ANIMATED GIF                   output          GRAPHICAL DISPLAy of radar data
#_________________________________________________________________________________________________
#=================================================================================================
#
#=================================================================================================
#-
#
# Programmer: Mr. Paul McCrone     11 August 2016
#             NOTE:
#                  While Mr. McCrone wrote the PYTHON code, the -C- code and IDL Code
#                  were originally written by Dr. Paul Harasti of Naval Research Lab.
#                  This PYTHON program will control the overall flow and control of
#                  the data conversion and graphical production process, but it will
#                  call modified versions of the Harasti code (McCrone made the 
#                  modifications to the -C- and IDL code.) 
#
# Modification  :  BELOW
#========================================================================================
#  Version 1.0   , Dated 2016-Aug-11
#                  Initial Build.
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  Version 2.0   , Dated 2016-Oct-30
#                  Working version that used the older -C- code and IDL code.
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  Version 3.0   , Dated 2016-Nov-08
#                  New Build with PyART python module 
#
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  Version 3.1.4 , Dated 2017-Feb-09
#                  New Build with modifications for operational use (IOC).
#
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Version 3.1.5 , Dated 2017-Feb-15
#                  New Build with modifications for use on Beta --a4bu-l4--.
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Version 3.1.5.2 , Dated 2017-Feb-16
#                  New Build with modifications for use on Beta --a4bu-l4--.
#                  --Fixed RODN--
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  Version 3.2     , Dated 2018-Sep-19
#                  Modified the way the code selects Level II files.
#                 
#  - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# 
#========================================================================================
#  NOTE: THIS PROGRAM ASSUMES THE USE OF Python version 2.7.0+ for RHEL.
#---------------------------------------------------------------
#
#  PYTHON MODULES USED: numpy, scipy, matplotlib, datetime, PyART,
#                       os, sys, math, warnings, socket, commands
#  	
#---------------------------------------------------------------#
#
import numpy as NP
from numpy.random import randn
#
from matplotlib import use
use("agg")
#
import scipy as S
import matplotlib as MPL
import pandas as PD
import datetime
import os as OS
import sys as SYS
import math as MATH
import warnings as WARNINGS
import socket
import commands
import matplotlib.pyplot as plt
import pyart
#
#
#
#import matplotlib.pyplot as plt
#import mpl_toolkits.basemap as bm
#import plotly as PLY
#
WARNING_INIT_ERROR=1

#
DADASHES='-----------------------------------------------------'
dadash='-----------------------------------------------------'
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'
#
#current_working_directory='/home/mccronep/NEXRAD/python'
#current_working_directory='/satdat/m4b/NEXRAD/python'
#current_working_directory='/satdat/curr/NEXRAD/python'

#----------------------------------------------------------------
#
infromlinux = commands.getoutput('echo ${RADAR_BASEPATH}')
### RADAR_BASEPATH (should be)=/satdat/curr/NEXRAD/python/
#
my_RADAR_BASEPATH=infromlinux
#
    
#-----------------
    
if my_RADAR_BASEPATH== '':
    my_RADAR_BASEPATH='/satdat/curr/NEXRAD/python/'
    #
    #----------------------
    #----------------------------------------------------

current_working_directory='/satdat/curr/NEXRAD/python'
current_working_directory=my_RADAR_BASEPATH
#
#
CWD_PATH=current_working_directory+'/'
#
#
CONF_PATH=CWD_PATH+'conf/'
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
this_return_value = 0
valid_thispath=OS.path.exists(CONF_PATH)
if valid_thispath:
    print(dadash)
    print("This path is VALID and EXISTS:: "+CONF_PATH)
    this_return_value = 1
    WARNING_INIT_ERROR=1
    print(dadash)
    #
else:
    #
    print("--CAUTION--")
    print("You are requesting the validity of this path: "+thispath)
    print("-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
    this_return_value = 0
    WARNING_INIT_ERROR=0
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
program_name="nexrad_image_process.py"
#
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
HIT_file=CONF_PATH+"radar_nexrad_process.HIT.conf"
#
this_return_value = 0
#
# Check thisfile
#
valid_thisfile=OS.path.isfile(HIT_file)
#
if valid_thisfile:
    print(dadash)
    print("This file is VALID and EXISTS:: "+HIT_file)
    this_return_value = 1
    print(dadash)
    WARNING_INIT_ERROR=1
    #
else:
    #
    print("---CAUTION---")
    print("---The indicated file is INVALID! NEED TO CHECK THIS!: "+HIT_file)
    this_return_value = 0
    WARNING_INIT_ERROR=0
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
####==================================================
#
# Read in the HIT list from the config file
#
# The config file --radar_nexrad_process.HIT.conf-- 
# is just a list of RADAR sites [the four letter 
# identifiers, like KAMX for Miami.] There should
# be only a list of four letter identifiers, 
# and nothing else. There shold be no more than
# 33 sites in this list.
#
####=================================================
#
try:
    with open(HIT_file,'r') as f:
        data_HIT_list=f.readlines()
except:
    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#
#
#>>> data_HIT_list
#['PGUA\n', 'RKJK\n', 'RKSG\n', 'TJUA\n', 'PHKI\n', 'PHKM\n', 
# 'PHMO\n', 'PHWA\n', 'KBOX\n', 'KDIX\n', 'KDOX\n', 'KAKQ\n', 
# 'KMHX\n', 'KJAX\n', 'KLTX\n', 'KCLX\n', 'KNKX\n', 'KMLB\n', 
# 'KAMX\n', 'KBYX\n', 'KTLH\n', 'KTBW\n', 'KEVX\n', 'KMOB\n', 
# 'KLIX\n', 'KLCH\n', 'KHGX\n', 'KBRO\n', 'KCRP\n', 'KOKX\n', 
# 'KLGX\n', 'KMUX\n']
#
#======================
#
####==================================================
#
# Having read in the RADAR sites from the conf file, 
# note that the reading process appends a return
# character [--backslash n--] at the end of each
# four letter identifier. We don't want this. We need
# to eliminate the return character.  So a given item
# in the list is:
#                 >>> data_HIT_list[0]
#                     'PGUA\n'
#
# Note the --backslash n-- at the end of the string.
# To eliminate the --backslash n--, we will only
# take the first four characters of this string,
# and use that, see below for examples:
#.
#                 >>> data_HIT_list[0][0:3]
#                     'PGU'
#                 >>> data_HIT_list[0][0:4]
#                     'PGUA'
#
# We will append each item to the list --HIT_call_signs--
# Which is the -High Interest Target- RADAR list,
# which will be referred to as the -HIT- list.
# ------------------------------------------------
# Note: this python program will only process the 
# RADAR sites that are identified in the list 
# --HIT_call_signs--, and not ALL 160 NEXRAD sites.
#
# ------------------------------------------------
# It is important to NOT process more than 33 sites
# with this program because we are trying to process all
# HIT List in 20 minutes or less, and 33 is the normal
# maximum number that this program can handle while
# remaining inside the 20 minute limit.
#
####==================================================
#
#
#HIT_call_signs=['PGUA']
HIT_call_signs=['RODN']
#
# Note on above line: I start the list with RODN --which is Kadena--
#                     in the python code itself on purpose  
#                     so it never needs to be added to the HIT list.
#                     configuration file, though adding it will not
#                     hurt anything --it would just get processed again--
#
#
for eachitem in data_HIT_list:
    HIT_call_signs.append(eachitem[0:4])
#   The [0:4] part above is to eliminate the return character
#   from the data file.
#
#
#
#list_of_lats = np.arange(0.0,90.0,1.0)
list_of_lats = NP.arange(0.0,90.0,1.0)
#
#list_of_lons =np.arange(-179.0,181.0,1.0)
list_of_lons =NP.arange(-179.0,181.0,1.0)
#

#HIT_call_signs= \
#['PGUA','RKJK','RKSG','TJUA','PHKI','PHKM','PHMO','PHWA', \
#'KBOX','KDIX','KDOX','KAKQ','KMHX','KJAX', \
#'KLTX','KCLX','KNKX','KMLB','KAMX','KBYX','KTLH', \
#'KTBW','KEVX','KMOB','KLIX','KLCH','KHGX','KBRO','KCRP','KOKX','KLGX','KMUX']
##
#
# 'KOKX',
#
#
# DELETED: 
#
ALL_call_signs= \
["PGUA","RKSG","RKJK","RODN","KABR","KENX","KABX","KFDR","KAMA","PAHG", \
"KEWX","KBBX","PABC","KBLX","KBGM","KBMX","KBIS","KCBX","KBOX","KBRO", \
"KBUF","KCXX","KFDX","KICX","KCLX","KRLX","KCYS","KLOT","KILN","KCLE", \
"KCAE","KGWX","KCRP","KFWS","KDVN","KFTG","KDMX","KDTX","KDDC","KDOX", \
"KDLH","KDYX","KEYX","KEVX","KEPZ","KLRX","KBHX","PAPD","KFSX","KHPX", \
"KGRK","KPOE","KEOX","KSRX","KIWX","KAPX","KGGW","KGLD","KMVX","KGJX", \
"KGRR","KTFX","KGRB","KGSP","KRMX","KUEX","KHDX","KCBW","KHGX","KHTX", \
"KIND","KJKL","KJAN","KJAX","PHKN","KEAX","KBYX","PAKC","KMRX","KARX", \
"LPLA","KLCH","KESX","KDFX","KILX","KLZK","KVTX","KLVX","KLBB","KMQT", \
"KMXX","KMAX","KMLB","KNQA","KAMX","PAIH","KMAF","KMKX","KMPX","KMBX", \
"KMSX","KMOB","PHMO","KVAX","KMHX","KOHX","KLIX","KOKX","PAEC","KAKQ", \
"KLNX","KTLX","KOAX","KPAH","KPDT","KDIX","KIWA","KPBZ","KSFX","KGYX", \
"KRTX","KPUX","KRAX","KUDX","KRGX","KRIW","KFCX","KJGX","KDAX","KLSX", \
"KMTX","KSJT","KNKX","KMUX","KHNX","TJUA","KSOX","KATX","KSHV","KFSD", \
"PACG","PHKI","PHWA","KOTX","KSGF","KCCX","KLWX","KTLH","KTBW","KTWX", \
"KEMX","KINX","KVNX","KVBX","KICT","KLTX","KFFC","KYUX","KLGX"]
#
#
#
#
dict_call_signs={"KABR":"Aberdeen_SD", "KABX":"Albuquerque_NM", "KAKQ":"Norfolk-VA", \
"KAMA":"Amarillo_TX", "KBBX":"Beale-AFB_CA", \
"KAMX":"Miami-FL", "KAPX":"Gaylord_MI", "KARX":"La-Crosse_WI", "KATX":"Seattle-Tacoma_WA", \
"KBGM":"Binghamton_NY", "KBHX":"Eureka_CA", "KBIS":"Bismarck_ND", "KBLX":"Billings_MT", \
"KBMX":"Birmingham_AL", "KCAE":"Columbia_SC", \
"KBOX":"Boston-MA", "KBRO":"Brownsville-TX", "KBUF":"Buffalo_NY", "KBYX":"Key-West-FL", \
"KCBW":"Houlton-Maine", "KCBX":"Boise_ID", "KCCX":"State-College_PA", "KCLE":"Cleveland_OH", \
"KCLX":"Charleston-SC", "KDDC":"Dodge-City_KS", \
"KCRP":"Corpus-Christi-TX", "KCXX":"Burlington_VT", "KCYS":"Cheyenne_WY", "KDAX":"Sacramento_CA", \
"KDFX":"Laughlin-AFB_TX", "KDIX":"Philadelphia-PA", "KDLH":"Duluth_MN", "KDMX":"Des-Moines_IA", \
"KDOX":"Dover-AFB-DE", "KEMX":"Tucson_AZ", \
"KDTX":"Detroit_MI", "KDVN":"Davenport_IA", "KDYX":"Dyess-AFB_TX", "KEAX":"Kansas-City_MO", \
"KENX":"Albany_NY", "KEOX":"Fort-Rucker_AL", "KEPZ":"El-Paso_TX", "KESX":"Las-Vegas_NV", \
"KEVX":"Eglin-AFB-FL", "KFDX":"Cannon-AFB_NM", \
"KEWX":"Austin-San-Antonio_TX", "KEYX":"Edwards-AFB_CA", "KFCX":"Roanoke_VA", "KFDR":"Altus-AFB_OK", \
"KFFC":"Atlanta_GA", "KFSD":"Sioux-Falls_SD", "KFSX":"Flagstaff_AZ","KFTG":"Denver_CO", \
"KFWS":"Dallas-Ft.Worth_TX", "KGRK":"Fort-Hood_TX", \
"KGGW":"Glasgow_MT", "KGJX":"Grand-Junction_Co", "KGLD":"Goodland_KS", "KGRB":"Green-Bay_WI", \
"KGRR":"Grand-Rapids_MI", "KGSP":"Greer_SC", "KGWX":"Columbus-AFB,_ MS", "KGYX":"Portland-Maine", \
"KHDX":"Holloman-AFB_NM", "KHTX":"Huntsville_AL",  \
"KHGX":"Houston-Galveston-TX", "KHNX":"San-Joaquin-Valley_CA", "KHPX":"Fort-Campbell_KY", \
"KICT":"Wichita_KS", "KICX":"Cedar-City_UT", "KILN":"Cincinnati_OH", "KILX":"Lincoln_IL", \
"KIND":"Indianapolis_IN", "KJAX":"Jacksonville-FL", \
"KINX":"Tulsa_OK", "KIWA":"Phoenix_AZ", "KIWX":"Fort-Wayne_IN", "KJAN":"Jackson_MS", \
"KJGX":"Robins-AFB_GA", "KJKL":"Jackson_KY", "KLBB":"Lubbock_TX", "KLCH":"Lake-Charles-LA", \
"KLIX":"New-Orleans-LA", "KLTX":"Wilmington-NC", \
"KLNX":"North-Platte_NE", "KLOT":"Chicago_IL", "KLRX":"Elko_NV", "KLSX":"Saint-Louis_ MO", \
"KLVX":"Louisville_KY", "KLWX":"Sterling-VA", "KLZK":"Little-Rock_AR", "KMAF":"Midland-Odessa_TX", \
"KMAX":"Medford_OR", "KMOB":"Mobile-AL", \
"KMBX":"Minot-AFB_ND", "KMHX":"Morehead-City-NC", "KMKX":"Milwaukee_WI", "KMLB":"Melbourne-FL", \
"KMPX":"Minneapolis-St.Paul_MN", "KMQT":"Marquette_MI", "KMRX":"Knoxville-Tri-Cities_TN", \
"KMSX":"Missoula_MT", "KNKX":"San-Diego-CA", \
"KMTX":"Salt-Lake-City_UT", "KMUX":"San-Francisco_CA", "KMVX":"Grand-Forks_ND", "KMXX":"Maxwell-AFB_AL", \
"KNQA":"Memphis_TN", "KOAX":"Omaha_NE", "KOHX":"Nashville_TN", "KOKX":"New-York-City-NY", \
"KOTX":"Spokane_WA", "KPAH":"Paducah_KY", \
"KPBZ":"Pittsburgh_PA", "KPDT":"Pendleton_OR", "KPOE":"Fort-Polk_LA", "KPUX":"Pueblo_CO", \
"KRAX":"Raleigh-Durham_NC", "KRGX":"Reno-NV", "KSFX":"Pocatello-Idaho-Falls_ID", \
"KRIW":"Riverton_WY", "KRLX":"Charleston_WV", "KRMX":"Griffiss-AFB_NY", "KRTX":"Portland_OR", \
"KSGF":"Springfield_MO", "KSHV":"Shreveport_LA", "KSJT":"San-Angelo_TX", \
"KSOX":"Santa-Ana_Mountains_CA", "KTLX":"Oklahoma-City_OK", \
"KSRX":"Fort-Smith_AR", "KTBW":"Tampa-FL", "KTFX":"Great-Falls_MT", "KTLH":"Tallahassee-FL", \
"KTWX":"Topeka_KS", "KUDX":"Rapid-City_SD", "KUEX":"Hastings_NE", "KVAX":"Moody-AFB_GA", \
"KVBX":"Vandenberg-AFB_CA", "PABC":"Bethel_AK", \
"KVNX":"Vance-AFB_OK", "KVTX":"Los_Angeles_CA", "KYUX":"Yuma_AZ", "LPLA":"Lajes-AB_Azores", \
"PACG":"Sitka_AK", "PAEC":"Nome_AK", "PAHG":"Anchorage_AK", "PAIH":"Middleton-Island_AK", 
"PAKC":"King-Salmon_AK", "PHKM":'Kamuela-Kohala-HI', \
"PAPD":"Fairbanks_AK", "PGUA":"Anderson-AFB-Guam", "PHKI":"South-Kauai-HI", \
"PHKN":"Kamuela_HI", "PHMO":"Molokai-HI", "PHWA":"South-Shore-HI", "RKJK":"Kunsan-AB-Korea", \
"RKSG":"Camp-Humphreys-Korea", "RODN":"Kadena_Okinawa", "TJUA":"San-Juan-Puerto-Rico", \
"KLGX":"Langley-Hill_WA"}


#
#
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
NEX_file=CWD_PATH+'NEXRAD_Data_LL_Data.csv'
#
this_return_value = 0
#
# Check thisfile
#
valid_thisfile=OS.path.isfile(NEX_file)
#
if valid_thisfile:
    print(dadash)
    print("This file is VALID and EXISTS:: "+NEX_file)
    this_return_value = 1
    print(dadash)
    WARNING_INIT_ERROR=1
    #
else:
    #
    print("---CAUTION---")
    print("---The indicated file is INVALID! NEED TO CHECK THIS!: "+NEX_file)
    this_return_value = 0
    WARNING_INIT_ERROR=0
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#
#nexrad_dataframe = PD.read_csv(CWD_PATH+'NEXRAD_Data.csv')
#nexrad_dataframe = PD.read_csv(CWD_PATH+'NEXRAD_Data_LLW.csv')
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
try:
    nexrad_dataframe = PD.read_csv(CWD_PATH+'NEXRAD_Data_LL_Data.csv')
except:
    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


sp='==>'

print DADASHES

#
#
#--------------------------------------
# nexrad_dataframe - > TABS:                                                                                       
# ----> WBAN 
# ----> STATION_ID
# ----> STATION_NAME 
# ----> LATN/LONGW(deg,min,sec)
# ----> ELEV(ft)
# ----> TOWER_HEIGHT(m)
# ----> TROPICAL
# ----> COASTAL
# ----> INLAND
# ----> LAT_N(deg,min,sec)
# ----> LONG_W(deg,min,sec)
#--------------------------------------
# ----> LATDfloat
# ----> LONGfloat
# ----> STATION_NAME
# ----> LAT
# ----> LONG
#--------------------------------------
#
#

try:
    nexrad_dataframe.set_index('STATION_ID')
except:
    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

print DADASHES

sp='==>'

print DADASHES
print DADASHES

#
# Here I will create a dataframe that contains the properly computed lats and longs
# Indexed by trhe RADAR site callsigns
#

LEN_ALL_call_signs=len(ALL_call_signs)

print dadash
print dadash


#------------------------------------------------------------
#
#------------------------------------------------------------
#
#------------------------------------
#============================================================

print DAEQUALS
print "The nexrad_dataframe"
print DAEQUALS
#
try:
    print nexrad_dataframe
except:
    WARNING_INIT_ERROR=0
#============================================================

print DAEQUALS
print DAEQUALS

#----------------------------------------
print dadash
#----------------------------------------
print dadash
#----------------------------------------
#----------------------------------------
##
#----------------------------------------
print dadash
print dadash
#----------------------------------------
#----------------------------------------
print DADASHES+DADASHES
print DADASHES+DADASHES
print DADASHES+DADASHES
#
#------------------------------------------------------------
#------------------------------------------------------------
print DADASHES
#
#
print DADASHES
print DADASHES

#------------------------------------------------------------
# END the mapping routine
#------------------------------------------------------------
#
#####------------------------------------------------------------------------------
#####  These are ALL the NEXRAD RADAR sites that are ingested from 557WW [AFWA]  
#####  These are moved to :
#####  a4ou-l4:/u/curr/etc/dynamic/obs_data/met/cqc/radar
#####------------------------------------------------------------------------------
#
# KABR  KBIS  KCLE  KDMX  KEVX  KGGW  KHNX  KJAX  KLTX  KMPX  KOHX  KRLX  KTLX  KTWX                 
# PACG  RKJK  KABX  KBLX  KCLX  KDOX  KEWX  KGJX  KHPX  KJGX  KLVX  KMQT  KOKX  KRTX                
# PAEC  RKSG  KAKQ  KBMX  KCRP  KDTX  KEYX  KGLD  KHTX  KJKL  KLWX  KMRX  KOTX  KSFX  
# KTYX  PAHG  TJUA  KAMA  KBOX  KCXX  KDVN  KFCX  KGRB  KICT  KLBB  KLZK  KMSX  KPAH  
# KSGF  KUDX  PAIH  KAMX  KBRO  KCYS  KDYX  KFDR  KGRK  KICX  KLCH  KMAF  KMTX  KPBZ  
# KSHV  KUEX  PAKC  KAPX  KBUF  KDAX  KEAX  KFDX  KGRR  KILN  KLGX  KMAX  KMUX  KPDT  
# KSJT  KVAX  PAPD  KARX  KBYX  KDDC  KEMX  KFFC  KGSP  KILX  KLIX  KMBX  KMVX  KPOE  
# KSOX  KVBX  PGUA  KATX  KCAE  KDFX  KENX  KFSD  KGWX  KIND  KLNX  KMHX  KMXX  KPUX  
# KSRX  KVNX  PHKI  KBBX  KCBW  KDGX  KEOX  KFSX  KGYX  KINX  KLOT  KMKX  KNKX  KRAX  
# KTBW  KVTX  PHKM  KBGM  KCBX  KDIX  KEPZ  KFTG  KHDX  KIWA  KLRX  KMLB  KNQA  KRGX  
# KTFX  KVWX  PHMO  KBHX  KCCX  KDLH  KESX  KFWS  KHGX  KIWX  KLSX  KMOB  KOAX  KRIW  
# KTLH  KYUX  PABC  PHWA
# 
######a4bu-l4:/u/curr/etc/dynamic/obs_data/met/cqc/radar >
#
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x
#  LIST OF PYTHON FUNCTIONS:
#--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x
#
#  ==> fxn()
#	--> Eliminate python warnings.
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Print_Current_Time(now)
#	--> INPUT <<now>>:String, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Access_Current_Time(now)
#       --> INPUT <<now>>:String, Output: Formatted String
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==>IS_This_Path_Valid(thispath) 
#	--> INPUT <<now>>:String, Output: Integer 
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Decompress_NEXRAD_File(my_XFER_BASEPATH)
#	--> INPUT <<my_XFER_BASEPATH>>: String/Path,  Output: Success/Failure
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Convert_NEXRAD_2_ASCII(my_XFER_BASEPATH)
#	--> INPUT <<my_XFER_BASEPATH>>: String/Path,  Output: Success/Failure
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> Display_NEXRAD_Graphics_IDL(my_XFER_BASEPATH)
#	--> INPUT <<my_XFER_BASEPATH>>: String/Path,  Output: Success/Failure
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> PyART_NEXRAD_DopVel(sourcedatapath, datapath, my_XFER_BASEPATH, RADAR_Callsign, my_RADAR_BASEPATH)
#       --> INPUT <Path info for making graphics>, Output: Graphic Files / Jpeg
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#  ==> PyART_NEXRAD_File(sourcedatapath, datapath, my_XFER_BASEPATH, RADAR_Callsign, my_RADAR_BASEPATH)
#       --> INPUT <Path info for making graphics>, Output: Graphic Files / Jpeg
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#
#  ==> main()
#       --> This is the -MAIN- program.
#       --> INPUT: <<--NONE-->>, OUTPUT: Execution Error codes.  
#  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
#--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x--x
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function fxn
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def fxn():
    WARNINGS.warn("nan", DeprecationWarning)
    #WARNINGS.warn("deprecated", DeprecationWarning)
    #WARNINGS.warn("Warning: converting a masked element to nan.", DeprecationWarning)
#######  END OF Function fxn

with WARNINGS.catch_warnings():
    WARNINGS.simplefilter("ignore")
    fxn()

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Print_Current_Time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Print_Current_Time(now):
    #-----
    ###import datetime
    #-----
    now = datetime.datetime.now()
    #-----
    print
    print "Current date and time using str method of datetime object:"
    print str(now)
    #-----
    print " \n"
    print "Current date and time using instance attributes:"
    print "Current year: %d" % now.year
    print "Current month: %d" % now.month
    print "Current day: %d" % now.day
    print "Current hour: %d" % now.hour
    print "Current minute: %d" % now.minute
    print "Current second: %d" % now.second
    print "Current microsecond: %d" % now.microsecond
    #-----
    print " \n"
    print "Current date and time using strftime:"
    #print now.strftime("%Y-%m-%d %H:%M")
    print now.strftime("%Y-%m-%d...%H:%M")
    #-----
    print " \n"
    print "Current date and time using isoformat:"
    print now.isoformat()
    return now.strftime("%Y-%m-%d...%H:%M")
    #return now
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Print_Current_Time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function IS_This_Path_Valid()
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def IS_This_Path_Valid(thispath):
    #-----
    # If this path is Valid, then say so [print in the affirmative]
    # return this_return_value=1
    # Otherwise, state that the path is invalid, then return this_return_value=0
    #.....................
    #
    this_return_value = 0
    #
    # Check thispath  
    #
    valid_thispath=OS.path.exists(thispath)

    if valid_thispath:
        print(dadash)
        print("You are requesting the validity of this path: "+thispath)
        print("This path is VALID and EXISTS")
        this_return_value = 1
        print(dadash)
        #
    else:
        #
        print("--CAUTION--")
        print("You are requesting the validity of this path: "+thispath)
        print("-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        this_return_value = 0
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    return this_return_value
    #
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF IS_This_Path_Valid    
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function IS_This_File_Valid()
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def IS_This_File_Valid(thisfile):
    #---------------------
    # If this file is Valid, then say so [print in the affirmative]
    # return this_return_value=1
    # Otherwise, state that the file is invalid, then return this_return_value=0
    #.....................
    #
    this_return_value = 0
    #
    # Check thisfile
    #
    valid_thisfile=OS.path.exists(thisfile)

    if valid_thisfile:
        print(dadash)
        print("You are requesting the validity of this File: "+thisfile)
        print("This file is VALID and EXISTS")
        this_return_value = 1
        print(dadash)
        #
    else:
        #
        print("--CAUTION--")
        print("You are requesting the validity of this file: "+thisfile)
        print("-------The indicated file is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
        this_return_value = 0
        #-----------------------------------------------------------
        # End of if block
        #-----------------------------------------------------------
    #.....................
    return this_return_value
    #
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF IS_This_File_Valid
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Access_Current_Time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Access_Current_Time(now):
    #-----
    ###import datetime
    #-----
    now = datetime.datetime.now()
    #-----
    print
    print "Current date and time using str method of datetime object:"
    print str(now)
    #-----
    print " \n"
    print "Current date and time using instance attributes:"
    print "Current year: %d" % now.year
    print "Current month: %d" % now.month
    print "Current day: %d" % now.day
    print "Current hour: %d" % now.hour
    print "Current minute: %d" % now.minute
    print "Current second: %d" % now.second
    print "Current microsecond: %d" % now.microsecond
    #-----
    print " \n"
    print "Current date and time using strftime:"
    #print now.strftime("%Y-%m-%d %H:%M")
    print now.strftime("%Y-%m-%d...%H:%M")
    #-----
    print " \n"
    print "Current date and time using isoformat:"
    print now.isoformat()
    return now.strftime("%Y-%m-%d.rapidscat.ncdf.%H-%M")
    #return now
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Access_Current_Time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
###---
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function PyART_NEXRAD_DopVel
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def PyART_NEXRAD_DopVel(sourcedatapath, datapath, my_XFER_BASEPATH, RADAR_Callsign, my_RADAR_BASEPATH):
    #
    print("Begin --PyART_NEXRAD_DopVel--")
    #
    error_code=1
    #
    print('The value of --sourcedatapath-- is: '+str(sourcedatapath))
    print('The value of -----datapath----- is: '+str(datapath))
    print('The value of -my_XFER_BASEPATH- is: '+str(my_XFER_BASEPATH))
    print('The value of --RADAR_Callsign-- is: '+str(RADAR_Callsign))
    #
    #
    #localpath='/satdat/m4b/NEXRAD/python/'
    #localpath='/satdat/curr/NEXRAD/python/'
    localpath=my_RADAR_BASEPATH
    #
    #
    check_path = 0
    check_path = IS_This_Path_Valid(localpath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --localpath --  : "+str(localpath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    data_in_path=my_RADAR_BASEPATH+'../../data_in/'
    #
    #
    check_path = 0
    check_path = IS_This_Path_Valid(data_in_path)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --data_in_path --  : "+str(data_in_path)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #utilpath='/satdat/m4b/NEXRAD/NEXRAD_Display/util/'
    #utilpath='/satdat/curr/NEXRAD/NEXRAD_Display/util/'
    utilpath=my_RADAR_BASEPATH+'../NEXRAD_Display/util/'
    #
    #
    check_path = 0
    check_path = IS_This_Path_Valid(utilpath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --utilpath --  : "+str(utilpath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    # The --sitesourcepath-- is the location of the compressed
    # level 2 data that will be processed.
    # We will move the last 5 files from --sitesourcepath-- to
    # datapath.
    #
    sitesourcepath=sourcedatapath+RADAR_Callsign+'/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(sitesourcepath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --sitesourcepath --  : "+str(sitesourcepath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    contents_sourcepath=OS.listdir(sitesourcepath)
    lencspath=len(contents_sourcepath)
    #
    if (lencspath < 5):
        #
        print(dadash+dadash)
        print("ERROR: The path --sitesourcepath --  : "+str(sitesourcepath)+" has no data. Nothing to process.")
        print(dadash+dadash)
        this_execution=77
        return this_execution
    else:
        print("The --sitesourcepath --  : "+str(sitesourcepath)+" HAS  DATA FILES... PROCESSING CONTINUES...")
        #---------------------
        # END of IF Block
        #---------------------

    print(dadash+dadash)
    print("---contents_sourcepath---")
    print(dadash+dadash)
    #
    print contents_sourcepath
    print(dadash+dadash)
    print(dadash+dadash)
    #
    #
    # == == == == == == == == == == == == == == == == == == ==
    #
    # == == == == == == == == == == == == == == == == == == ==
    #
    #my_NEXRAD_decompress=my_XFER_BASEPATH+'/../../m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Decompress/'
    #
    #JPEG_dir='/satdat/m4b/NEXRAD/python/JPEGtest/'
    #JPEG_dir='/satdat/m4b/NEXRAD/python/JPEG/'
    #JPEG_dir='/satdat/curr/NEXRAD/python/JPEG/'
    JPEG_dir=localpath+'JPEG/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(JPEG_dir)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --JPEG_dir--  : "+str(JPEG_dir)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    GTIFF_dir=localpath+'GeoTIFF/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(GTIFF_dir)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --GTIFF_dir--  : "+str(GTIFF_dir)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    # Convert Level II Binary data to ASCII (Location of -C- binaries):
    # /satdat/m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process
    # == == == == == == == == == == == == == == == == == == ==
    #
    #my_NEXRAD_ascii=my_XFER_BASEPATH+'/../../m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process/'
    my_NEXRAD_ascii=my_XFER_BASEPATH+'/../NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_NEXRAD_ascii)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --my_NEXRAD_ascii--  : "+str(my_NEXRAD_ascii)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    #----------------------------------------------------
    #----------------------------------------------------
    #----------------------------------------------------
    #
    #<<<<CODE GOES HERE>>>>>>>
    #
    #localpath='/satdat/curr/NEXRAD/python/'

    templist_of_files=utilpath+"file_list.txt.temp"

    tmpl_templist_of_files=utilpath+"template_file_list.txt.temp"

    tmpl_list_of_5_files = utilpath+"template_file_5_list.txt"

    #
    #list_of_2_files =['0','1']
    #
    list_of_1_files =['0']
    original_1_files =['0']
    destin_1_files =['0']
    #
    #
    list_of_1_files[0] = contents_sourcepath[lencspath-1]
    #
    # sitesourcepath
    # sitesourcepath
    #
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Will now determine the most recent file in the -sitesourcepath-.
    # That file will be stored in list_of_1_files[0].
    # The method above does not always get the most recent file.
    # Change made: Sept 19, 2018 PJM
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #
    pythonhome=localpath
    cmd_str='ls -Art '+sitesourcepath+' *.compress.*  | tail -n 1 > '+pythonhome+'tmp'
    tmpfile=pythonhome+'tmp'
    OS.system(cmd_str)
    result=open(tmpfile, 'r').read()
    #
    print(dadash+dadash)
    print("Selcted datafile: "+result)
    print(dadash+dadash)
    #
    list_of_1_files[0] = result
    #
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #
    derivedatafrom = list_of_1_files[0]
    #
    # 20161108190900.compress.raw
    #
    yymmdd='d'+derivedatafrom[0:8]
    hhmmss='s'+derivedatafrom[8:14]
    #
    #
    print('The year-month-day     is: '+yymmdd)
    print('The hour-minute-second is: '+hhmmss)
    #
    #
    yyyy_mm_dd = derivedatafrom[0:4]+'-'+derivedatafrom[4:6]+'-'+derivedatafrom[6:8]
    #
    hh_MM_sec  = derivedatafrom[8:10]+':'+derivedatafrom[10:12]+':'+derivedatafrom[12:14]
    #
    print('The year-month-day -2-     is: '+yyyy_mm_dd)
    #
    print('The hour-minute-second -2- is: '+hh_MM_sec)
    #
    ymdhms_formatted = yyyy_mm_dd+'---'+hh_MM_sec+'_UTC'
    #
    print('Formatted Date-time String:')
    print(ymdhms_formatted)
    #
    #
    original_1_files[0] = sitesourcepath+contents_sourcepath[lencspath-1]
    #
    destin_1_files[0] = datapath+contents_sourcepath[lencspath-1]
    #
    list_of_1 = [0]
    #
    #-----------------------
    #
    #
    print("---List of 1 files---")
    print(str(list_of_1_files))
    #
    l1temp=['0','0','0']
    #
    lo1_files =['0']
    lo1_files_wpath =['0']
    #
    for item in list_of_1:
        #
        original = original_1_files[item]
        #
        destination = destin_1_files[item]
        #
        linux_cmd='cp -R '+original+' '+destination
        the_files=OS.system(linux_cmd)
        #
        linux_cmd='chmod 777 '+destination
        the_files=OS.system(linux_cmd)
        #
        l1temp=list_of_1_files[item].split('.')
        #
        lo1_files[item] = RADAR_Callsign+'_'+l1temp[0]+'.'+l1temp[2]
        #
        lo1_files_wpath[item] = datapath+lo1_files[item]
        #
        #---------------------------------
        # END OF FOR LOOP
        #---------------------------------
    #
    print("---lo1_files---")
    print(str(lo1_files))
    #
    #
    # sitesourcepath
    #
    title_string='/u/uuuu/uuu/uuuuuuu/uuuuuuuu/u2u/u3u/uu-uu/SIGN/file'
    #
    #
    print ("The PyArt  commands are executing as follows:.....")

    for item in list_of_1:
        #
        my_compressed_file=destin_1_files[item]
        #
        #
        print (".............................................................")
        #
        #radar = pyart.io.read(filename)
        #
        print('- - - - - - - - - - - - -')
        print('--my_compressed_file-- is: '+my_compressed_file)
        print('- - - - - - - - - - - - -')
        print('Reading file via pyart.io.read')
        #
        #
        read_radar_ok = 1
        #
        #
        try:
            radar = pyart.io.read(my_compressed_file)
        except:
            read_radar_ok = 0
            print("WARNING: Error reading Level II datafile: "+my_compressed_file)
            continue
        #=================================================================#
        # Do not continue unless the Level II file was read in properly.
        #=================================================================#
        if (read_radar_ok  == 1):
            #
            SITE_latitude = radar.latitude['data'][0]
            #
            SITE_longitude  = radar.longitude['data'][0]
            #
            minlon=SITE_longitude-4.5
            maxlon=SITE_longitude+4.5
            #
            minlat=SITE_latitude-3.5
            maxlat=SITE_latitude+3.5
            #
            local_lats=[]
            local_lons=[]

            for item in list_of_lats:
                #
                if (item > minlat ) & (item < maxlat):
                    local_lats.append(item)
                    #---------------------------------
                    # END OF IF LOOP
                    #---------------------------------
                #---------------------------------
                # END OF FOR LOOP
                #---------------------------------
            #
            print('List of lats for grid plotting:')
            print(local_lats)
            #
            for item in list_of_lons:
                #
                if (item > minlon ) & (item < maxlon):
                    local_lons.append(item)
                    #---------------------------------
                    # END OF IF LOOP
                    #---------------------------------
                #---------------------------------
                # END OF FOR LOOP
                #---------------------------------

            print('List of lons for grid plotting:')
            print(local_lons)
            #
            #
            #RADAR_Callsign
            #
            PlaceName = 'Brownsville TX'
            PlaceName = dict_call_signs[RADAR_Callsign]
            #
            #GIS_shapefile = '/satdat/m4b/NEXRAD/python/shape/cb_2015_us_county_500k'
            #GIS_shapefile = '/satdat/curr/NEXRAD/python/shape/cb_2015_us_state_500k'
            GIS_shapefile = localpath+'shape/cb_2015_us_state_500k'
            #
            display = pyart.graph.RadarMapDisplay(radar)
            #
            # plot the second tilt
            #
            #-------------------------------------------------------------------------
            display.plot_ppi_map('velocity', 1, vmin=-50, vmax=50, min_lon=minlon, max_lon=maxlon, \
                min_lat=minlat, max_lat=maxlat, \
                lat_lines = local_lats, lon_lines = local_lons, \
                shapefile=GIS_shapefile, cmap='pyart_NWSVel',\
                projection='lcc', resolution='h', \
                lat_0=radar.latitude['data'][0],lon_0=radar.longitude['data'][0])
            #-------------------------------------------------------------------------
            #
            ## plot range rings at 50, 100, 200, 300 and 400km
            #
            #
            display.plot_range_ring(50., line_style='k--')
            display.plot_range_ring(100., line_style='k-',color='blue')
            display.plot_range_ring(200., line_style='k--',color='blue')
            #display.plot_range_ring(202., line_style='k-')
            display.plot_range_ring(300., line_style='k-',color='red')
            display.plot_range_ring(400., line_style='k--',color='red')
            #display.plot_range_ring(402., line_style='k-')
            #
            # plots cross hairs
            #
            display.plot_line_xy(NP.array([-100000.0, 100000.0]), NP.array([0.0, 0.0]), line_style='k-')
            #
            display.plot_line_xy(NP.array([0.0, 0.0]), NP.array([-100000.0, 100000.0]), line_style='k-')
            #
            # Indicate the radar location with a point
            #
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0])
            #
            display.plot_grid_lines(ax=None, col='k', ls=':')
            #
            #
            my_text1='                                                        400 km - - - - -  400 km '
            my_text2='200 km - - - - -  200 km '
            #
            display.plot_label(my_text1, (0,0) , symbol='r+', text_color='red', ax=None)
            display.plot_label(my_text2, (0,0) , symbol='r+', text_color='blue', ax=None)
            #
            #
            fileformat='.jpg'
            #
            JPEG_file_data='nexrad_'+RADAR_Callsign+'_'+yymmdd+'_'+hhmmss+'_'+'UTC_Base_DVelo'
            #
            TITLE_TEXT_1='NEXRAD Reflectivity '
            #
            TITLE_TEXT_2=RADAR_Callsign+' - '+PlaceName
            #
            plt.title(TITLE_TEXT_2+': '+ymdhms_formatted)
            #
            JPEG_filename=JPEG_dir+JPEG_file_data+fileformat
            #
            plt.savefig(JPEG_filename)
            #
            ###==============================
            ### Now start making the GeoTIFF
            ###==============================
            #
            ref_field ='reflectivity'                                 
            #
            GTIFF_fileformat='_GT.tif'
            #
            #GTIFF_dir='/home/satops/mccrone/python/src/RADAR_SWR/GeoTIFF/'
            #GTIFF_dir='/satdat/curr/NEXRAD/python/GeoTIFF/'
            #GTIFF_dir=localpath+'GeoTIFF/'
            #
            #
            Call_letters=RADAR_Callsign
            #
            #
            #JPEG_file_data='nexrad_GT_'+Call_letters+'_'+ymdhms_formatted
            JPEG_file_data='nexrad_GT_'+RADAR_Callsign+'_'+yymmdd+'_'+hhmmss+'_'+'UTC_Base_DVelo'
            #
            GTIFF_filename=GTIFF_dir+JPEG_file_data+GTIFF_fileformat
            #
            test_write_gtiff=1
            #
            #
            #=================================================================#
            # The overview of this section is that we peform a GateFilter
            # method on the -radar- object to prepare it for gridding.
            #
            # Gridding is necessary prior to making the GeoTIFF. 
            # The GeoTIFF production method assumes a gridded data set.
            #
            # Finally, the write_grid_geotiff is perfomed to make the geotiff.
            #
            #=================================================================#
            try:
                # exclude masked gates from the gridding
                gatefilter = pyart.filters.GateFilter(radar)
                gatefilter.exclude_transition()             
                gatefilter.exclude_masked('reflectivity')   
                print("NOTICE: performing gatefilter function-- ")
            except:                                               
                test_write_gtiff=0                                
                print("WARNING: Error with gatefilter operation ")
            #=================================================================#
            #=================================================================#
            try:
                radar_grid=pyart.map.grid_from_radars( \
                    (radar,), gatefilters=(gatefilter, ), \
                    grid_shape=(1, 241, 241), \
                    grid_limits=((2000, 2000), (-123000.0, 123000.0), (-123000.0, 123000.0)), \
                    fields=['reflectivity'])
                print("NOTICE: performing grid function-- ")
            except:
                test_write_gtiff=0
                print("WARNING: Error with grid operation....  ")
            #=================================================================#
            #=================================================================#
            try:
                pyart.io.write_grid_geotiff(radar_grid, filename=GTIFF_filename, field=ref_field , rgb=True, cmap='pyart_NWSRef')
                print("NOTICE: writing GeoTIFF:--> "+GTIFF_filename)
            except:
                test_write_gtiff=0
                print("WARNING: Error writing GeoTIFF:::: "+GTIFF_filename)
            #=================================================================#
            #
            ###==============================
            #
            plt.close()
            #---------------------
            # END of IF Block: read_radar_ok
            #---------------------
            #---------------------
        #=================================================================#
        #
        #
        #---------------------------------
        # END OF FOR LOOP
        #---------------------------------
    #
    #
    the_files=1
    #
    if (read_radar_ok  == 1):
        #
        #
        linux_cmd='cp '+JPEG_filename+' '+data_in_path
        the_files=OS.system(linux_cmd)
        #
        linux_cmd='cp '+GTIFF_filename+' '+data_in_path  
        the_files=OS.system(linux_cmd)
        #
        linux_cmd='rm -rf '+datapath+'*.compress.*'
        the_files=OS.system(linux_cmd)
        #
        if (the_files == 0):
            print('The files were deleted successfully.')
        else:
            print('NOTICE: THE FILE DELETIONs DID NOT OCCUR!!!')
            #---------------------
            # END of IF Block
            #---------------------
    #---------------------
    # END of IF Block
    #---------------------

    #
    #
    #
    print("END --PyART_NEXRAD_DopVel--")
    #
    return error_code
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF PyART_NEXRAD_DopVel
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#, my_RADAR_BASEPATH
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function PyART_NEXRAD_File
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def PyART_NEXRAD_File(sourcedatapath, datapath, my_XFER_BASEPATH, RADAR_Callsign, my_RADAR_BASEPATH):
    #
    print("Begin --Decompress_NEXRAD_File--")
    #
    error_code=1
    #
    print('The value of --sourcedatapath-- is: '+str(sourcedatapath))
    print('The value of -----datapath----- is: '+str(datapath))
    print('The value of -my_XFER_BASEPATH- is: '+str(my_XFER_BASEPATH))
    print('The value of --RADAR_Callsign-- is: '+str(RADAR_Callsign))
    #
    #
    #localpath='/satdat/m4b/NEXRAD/python/'
    localpath=my_RADAR_BASEPATH
    #
    check_path = 0
    check_path = IS_This_Path_Valid(localpath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --localpath --  : "+str(localpath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    data_in_path=my_RADAR_BASEPATH+'../../data_in/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(data_in_path)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --data_in_path --  : "+str(data_in_path)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #utilpath='/satdat/curr/NEXRAD/NEXRAD_Display/util/'
    utilpath=my_RADAR_BASEPATH+'../NEXRAD_Display/util/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(utilpath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --utilpath --  : "+str(utilpath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    # The --sitesourcepath-- is the location of the compressed
    # level 2 data that will be processed.
    # We will move the last 5 files from --sitesourcepath-- to
    # datapath.
    #
    sitesourcepath=sourcedatapath+RADAR_Callsign+'/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(sitesourcepath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --sitesourcepath --  : "+str(sitesourcepath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    contents_sourcepath=OS.listdir(sitesourcepath)
    lencspath=len(contents_sourcepath)
    #
    if (lencspath < 5):
        #
        print(dadash+dadash)
        print("ERROR: The path --sitesourcepath --  : "+str(sitesourcepath)+" has no data. Nothing to process.")
        print(dadash+dadash)
        this_execution=77
        return this_execution
    else:
        print("The --sitesourcepath --  : "+str(sitesourcepath)+" HAS  DATA FILES... PROCESSING CONTINUES...")
        #---------------------
        # END of IF Block
        #---------------------

    print(dadash+dadash)
    print("---contents_sourcepath---")
    print(dadash+dadash)
    #
    print contents_sourcepath
    print(dadash+dadash)
    print(dadash+dadash)
    #
    #
    # == == == == == == == == == == == == == == == == == == ==
    #
    # == == == == == == == == == == == == == == == == == == ==
    #
    #my_NEXRAD_decompress=my_XFER_BASEPATH+'/../../m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Decompress/'
    #
    #JPEG_dir='/satdat/curr/NEXRAD/python/JPEG/'
    JPEG_dir=localpath+'JPEG/'
    #
    #
    check_path = 0
    check_path = IS_This_Path_Valid(JPEG_dir)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --JPEG_dir--  : "+str(JPEG_dir)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    GTIFF_dir=localpath+'GeoTIFF/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(GTIFF_dir)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --GTIFF_dir--  : "+str(GTIFF_dir)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    # Convert Level II Binary data to ASCII (Location of -C- binaries):
    # /satdat/m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process
    # == == == == == == == == == == == == == == == == == == ==
    #
    #my_NEXRAD_ascii=my_XFER_BASEPATH+'/../../m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process/'
    my_NEXRAD_ascii=my_XFER_BASEPATH+'/../NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_NEXRAD_ascii)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --my_NEXRAD_ascii--  : "+str(my_NEXRAD_ascii)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #----------------------------------------------------
    #----------------------------------------------------
    #----------------------------------------------------
    #
    #<<<<CODE GOES HERE>>>>>>>
    #
    #localpath='/satdat/m4b/NEXRAD/python/'
    #localpath='/satdat/curr/NEXRAD/python/'

    templist_of_files=utilpath+"file_list.txt.temp"

    tmpl_templist_of_files=utilpath+"template_file_list.txt.temp"

    tmpl_list_of_5_files = utilpath+"template_file_5_list.txt"
    #
    #
    list_of_1_files =['0']
    original_1_files =['0']
    destin_1_files =['0']
    #
    #
    list_of_1_files[0] = contents_sourcepath[lencspath-1]
    #
    #
    #
    # sitesourcepath
    # sitesourcepath
    #
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Will now determine the most recent file in the -sitesourcepath-.
    # That file will be stored in list_of_1_files[0].
    # The method above does not always get the most recent file.
    # Change made: Sept 19, 2018 PJM
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #
    pythonhome=localpath
    cmd_str='ls -Art '+sitesourcepath+' *.compress.*  | tail -n 1 > '+pythonhome+'tmp'
    tmpfile=pythonhome+'tmp'
    OS.system(cmd_str)
    result=open(tmpfile, 'r').read()
    #
    print(dadash+dadash)
    print("Selcted datafile: "+result)
    print(dadash+dadash)
    #
    list_of_1_files[0] = result
    #
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #
    #
    derivedatafrom = list_of_1_files[0]
    #
    # 20161108190900.compress.raw
    #
    yymmdd='d'+derivedatafrom[0:8]
    hhmmss='s'+derivedatafrom[8:14]
    #
    print('The year-month-day     is: '+yymmdd)
    print('The hour-minute-second is: '+hhmmss)
    #
    #
    #yyyy_mm_dd = derivedatafrom[0:4]+'_'+derivedatafrom[4:2]+'_'+derivedatafrom[6:2]
    yyyy_mm_dd = derivedatafrom[0:4]+'-'+derivedatafrom[4:6]+'-'+derivedatafrom[6:8]
    #
    #hh_MM_sec  = derivedatafrom[8:2]+':'+derivedatafrom[10:2]+':'+derivedatafrom[12:2]
    hh_MM_sec  = derivedatafrom[8:10]+':'+derivedatafrom[10:12]+':'+derivedatafrom[12:14]
    #
    print('The year-month-day -2-     is: '+yyyy_mm_dd)
    #
    print('The hour-minute-second -2- is: '+hh_MM_sec)
    #
    ymdhms_formatted = yyyy_mm_dd+'---'+hh_MM_sec+' UTC'
    #
    print('Formatted Date-time String:')
    print(ymdhms_formatted)
    #
    #
    original_1_files[0] = sitesourcepath+contents_sourcepath[lencspath-1]
    #
    destin_1_files[0] = datapath+contents_sourcepath[lencspath-1]
    #
    list_of_1 = [0]
    #
    #-----------------------
    #
    print("---List of 1 files---") 
    print(str(list_of_1_files))
    #
    l1temp=['0','0','0']
    #
    lo1_files =['0']
    lo1_files_wpath =['0']
    #
    for item in list_of_1:
        #
        original = original_1_files[item] 
        #
        destination = destin_1_files[item]
        #
        linux_cmd='cp -R '+original+' '+destination
        the_files=OS.system(linux_cmd)
        #
        linux_cmd='chmod 777 '+destination
        the_files=OS.system(linux_cmd)
        #
        l1temp=list_of_1_files[item].split('.')
        #
        lo1_files[item] = RADAR_Callsign+'_'+l1temp[0]+'.'+l1temp[2]
        #
        lo1_files_wpath[item] = datapath+lo1_files[item]
        #
        #---------------------------------
        # END OF FOR LOOP
        #---------------------------------
    #
    print("---lo1_files---")
    print(str(lo1_files))
    #
    # sitesourcepath
    #
    title_string='/u/uuuu/uuu/uuuuuuu/uuuuuuuu/u2u/u3u/uu-uu/SIGN/file'
    # 
    print ("The PyArt  commands are executing as follows:.....")

    for item in list_of_1:
        #
        my_compressed_file=destin_1_files[item]
        #
        print (".............................................................")
        #
        #radar = pyart.io.read(filename)
        #
        print('- - - - - - - - - - - - -')
        print('--my_compressed_file-- is: '+my_compressed_file)
        print('- - - - - - - - - - - - -')
        print('Reading file via pyart.io.read')
        #
        read_radar_ok = 1
        #
        try:
            radar = pyart.io.read(my_compressed_file)
        except:
            read_radar_ok = 0
            print("WARNING: Error reading Level II datafile: "+my_compressed_file)
            continue
        #=================================================================#
        # Do not continue unless the Level II file was read in properly.
        #=================================================================#
        if (read_radar_ok  == 1):
            #
            SITE_latitude = radar.latitude['data'][0]
            #
            SITE_longitude  = radar.longitude['data'][0]
            #
            minlon=SITE_longitude-4.5
            maxlon=SITE_longitude+4.5
            #
            minlat=SITE_latitude-3.5
            maxlat=SITE_latitude+3.5
            #
            local_lats=[]
            local_lons=[]

            for item in list_of_lats:
                #
                if (item > minlat ) & (item < maxlat):
                    local_lats.append(item)
                    #---------------------------------
                    # END OF IF LOOP
                    #---------------------------------
                #---------------------------------
                # END OF FOR LOOP
                #---------------------------------
            #
            print('List of lats for grid plotting:')
            print(local_lats)
            #
            for item in list_of_lons:
                #
                if (item > minlon ) & (item < maxlon):
                    local_lons.append(item)
                    #---------------------------------
                    # END OF IF LOOP
                    #---------------------------------
                #---------------------------------
                # END OF FOR LOOP
                #---------------------------------

            print('List of lons for grid plotting:')
            print(local_lons)
            #
            #
            #RADAR_Callsign
            #
            PlaceName = 'Brownsville TX'
            PlaceName = dict_call_signs[RADAR_Callsign]
            #
            #GIS_shapefile = '/satdat/m4b/NEXRAD/python/shape/cb_2015_us_county_500k'
            #GIS_shapefile = '/satdat/curr/NEXRAD/python/shape/cb_2015_us_state_500k'
            GIS_shapefile = localpath+'shape/cb_2015_us_state_500k'
            #
            display = pyart.graph.RadarMapDisplay(radar)
            #
            # plot the second tilt
            #
            display.plot_ppi_map('reflectivity', 1, vmin=-32, vmax=64, min_lon=minlon, max_lon=maxlon, \
                min_lat=minlat, max_lat=maxlat, \
                lat_lines = local_lats, lon_lines = local_lons, \
                shapefile=GIS_shapefile, \
                projection='lcc', resolution='h', \
                lat_0=radar.latitude['data'][0],lon_0=radar.longitude['data'][0])

            #
            ## plot range rings at 50, 100, 200, 300 and 400km
            #
            display.plot_range_ring(50., line_style='k--')
            display.plot_range_ring(100., line_style='k-',color='blue')
            display.plot_range_ring(200., line_style='k--',color='blue')
            #display.plot_range_ring(202., line_style='k-')
            display.plot_range_ring(300., line_style='k-',color='red')
            display.plot_range_ring(400., line_style='k--',color='red')
            #display.plot_range_ring(402., line_style='k-')
            #
            # plots cross hairs
            #
            display.plot_line_xy(NP.array([-100000.0, 100000.0]), NP.array([0.0, 0.0]), line_style='k-')
            #
            display.plot_line_xy(NP.array([0.0, 0.0]), NP.array([-100000.0, 100000.0]), line_style='k-')
            #
            # Indicate the radar location with a point
            #
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0])
            #
            display.plot_grid_lines(ax=None, col='k', ls=':')
            #
            #
            my_text1='                                                        400 km - - - - -  400 km '
            my_text2='200 km - - - - -  200 km '
            #
            ##display.plot_label(my_text1, (SITE_latitude,SITE_longitude) , symbol='r+', text_color='red', ax=None)
            ##display.plot_label(my_text2, (SITE_latitude,SITE_longitude) , symbol='r+', text_color='blue', ax=None)
            #
            display.plot_label(my_text1, (0,0) , symbol='r+', text_color='red', ax=None)
            display.plot_label(my_text2, (0,0) , symbol='r+', text_color='blue', ax=None)
            #
            #
            #
            #JPEG_dir='/satdat/m4b/NEXRAD/python/JPEG/'
            #JPEG_dir='/satdat/curr/NEXRAD/python/JPEG/'
            #
            fileformat='.jpg'
            #
            JPEG_file_data='nexrad_'+RADAR_Callsign+'_'+yymmdd+'_'+hhmmss+'_'+'UTC_Base_Refl'           
            #
            TITLE_TEXT_1='NEXRAD Reflectivity '
            #
            TITLE_TEXT_2=RADAR_Callsign+' - '+PlaceName
            #
            #plt.title(TITLE_TEXT_1+TITLE_TEXT_2)
            plt.title(TITLE_TEXT_2+': '+ymdhms_formatted)

            #
            #plt.text(0.0, 1.0,ymdhms_formatted)
            #plt.text(0.0, 1.0,ymdhms_formatted,bbox={'facecolor':'yellow','alpha':0.5,'pad':10})
            ###plt.text(50.0, 10.0,'NEXRAD',bbox={'facecolor':'pink','pad':10})
            #
            #
            JPEG_filename=JPEG_dir+JPEG_file_data+fileformat
            #
            plt.savefig(JPEG_filename)
            #
            the_files=1
            #
            linux_cmd='cp '+JPEG_filename+' '+data_in_path
            the_files=OS.system(linux_cmd)
            #
            #=================================================================================#
            #
            ###==============================
            ### Now start making the GeoTIFF
            ###==============================
            #
            ref_field ='reflectivity'
            #
            GTIFF_fileformat='_GT.tif'
            #
            #GTIFF_dir='/home/satops/mccrone/python/src/RADAR_SWR/GeoTIFF/'
            #GTIFF_dir='/satdat/curr/NEXRAD/python/GeoTIFF/'
            #GTIFF_dir=localpath+'GeoTIFF/'
            #
            #
            Call_letters=RADAR_Callsign
            #
            #
            #JPEG_file_data='NEXRAD_refl_GT_'+Call_letters+'_'+ymdhms_formatted
            JPEG_file_data='nexrad_GT_'+RADAR_Callsign+'_'+yymmdd+'_'+hhmmss+'_'+'UTC_Base_Refl'
            #
            #
            GTIFF_filename=GTIFF_dir+JPEG_file_data+GTIFF_fileformat
            #
            test_write_gtiff=1
            #
            #
            #=================================================================#
            # The overview of this section is that we peform a GateFilter
            # method on the -radar- object to prepare it for gridding.
            #
            # Gridding is necessary prior to making the GeoTIFF. 
            # The GeoTIFF production method assumes a gridded data set.
            #
            # Finally, the write_grid_geotiff is perfomed to make the geotiff.
            #
            #=================================================================#
            try:
                # exclude masked gates from the gridding
                gatefilter = pyart.filters.GateFilter(radar)
                gatefilter.exclude_transition()
                gatefilter.exclude_masked('reflectivity')
                print("NOTICE: performing gatefilter function-- ")
            except:
                test_write_gtiff=0
                print("WARNING: Error with gatefilter operation ")
            #=================================================================#
            #=================================================================#
            #=================================================================#
            try:
                radar_grid=pyart.map.grid_from_radars( \
                    (radar,), gatefilters=(gatefilter, ), \
                    grid_shape=(1, 241, 241), \
                    grid_limits=((2000, 2000), (-123000.0, 123000.0), (-123000.0, 123000.0)), \
                    fields=['reflectivity'])
                print("NOTICE: performing grid function-- ")
            except:
                test_write_gtiff=0
                print("WARNING: Error with grid operation....  ")
            #=================================================================#
            #=================================================================#
            try:
                pyart.io.write_grid_geotiff(radar_grid, filename=GTIFF_filename, field=ref_field , rgb=True, cmap='pyart_NWSRef')
                print("NOTICE: writing GeoTIFF:--> "+GTIFF_filename)
            except:
                test_write_gtiff=0
                print("WARNING: Error writing GeoTIFF:::: "+GTIFF_filename)
            #=================================================================#
            #
            ###==============================
            #
            #=================================================================================#
            #
            plt.close()
            #---------------------
            # END of IF Block: read_radar_ok
            #---------------------
        #=================================================================#
        #
        #
        #---------------------------------
        # END OF FOR LOOP
        #---------------------------------
    #
    #
    #
    the_files=1
    #
    if (read_radar_ok  == 1):
        #
        ##
        linux_cmd='cp '+JPEG_filename+' '+data_in_path
        the_files=OS.system(linux_cmd)
        ##
        linux_cmd='cp '+GTIFF_filename+' '+data_in_path
        the_files=OS.system(linux_cmd)
        #
        linux_cmd='rm -rf '+datapath+'*.compress.*'
        the_files=OS.system(linux_cmd)
        #
        if (the_files == 0):
            print('The files were deleted successfully.')
        else:
            print('NOTICE: THE FILE DELETIONs DID NOT OCCUR!!!')
            #---------------------
            # END of IF Block
            #---------------------
    #---------------------
    # END of IF Block
    #---------------------

            #---------------------
    #
    #
    #
    print("END --PyART_NEXRAD_File--")
    #
    return error_code
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF PyART_NEXRAD_File
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#:
#:
########################################################################################################
########################################################################################################
#### BEGINNING OF MAIN FUNCTION ########################################################################
########################################################################################################
########################################################################################################
#######-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
#######  Begin MAIN Function for processing NEXRAD file
#######-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
#######
#######

def main():

    #
    dadots='.  .  .  .  .  .  .  .  .  .  .  .  .'
    dadash='-------------------------------------'
    dddots='.....................................'
    dastar='*************************************'
    dahash='#####################################'
    #
    #
    print(dadash+dadash)
    print(dadash+dadash)
    #
    right_now=0
    #
    the_start_time = Print_Current_Time(right_now)
    #
    print(" \n")
    print(dadash+dadash)
    print(dadash+dadash)
    #
    print('---BEGINNING THE --MAIN[]-- FUNCTION  -----')
    #
    #
    NOT_A_NUMBER=float('nan')
    #  MATH.isnan(NOT_A_NUMBER)
    #
    #
    #----------------------------------------------------
    print(dadash)
    #
    #----------------------------------------------------------------------------
    # Determine the paths of data:
    #   datapath:     	This is where the NETCDF from NASA files are stored.
    #   datarootpath:  	This is where the NETCDF from NASA files are stored.
    #   graphicpath:	This is the location where graphics are saved.
    #   ascii_path:   	This is where the ASCII version of the data is stored.
    #   binpath:	This is the location of this python source code.
    #   utilpath:       This is a utility subdirectory under the binpath.
    #   procpath:       This is a subdirectory that logs the NETCDF files already processed.
    #----------------------------------------------------------------------------
    #
    myhostname=socket.gethostname()
    thehost=myhostname[0:4]
    #
    infromlinux = commands.getoutput('echo ${OPSBIN}')		### /satdat/bin
    #                                                           ### /u/ops/bin
    #
    my_OPSBIN=infromlinux
    #
    #-----------------
    if my_OPSBIN== '':
        my_OPSBIN='/satdat/bin'
        #----------------------
        if thehost == "a4bu":
            my_OPSBIN='/u/ops/bin'
            #
        #----------------------
        if thehost == "a4ou":
            my_OPSBIN='/u/ops/bin'
            #
        #----------------------
        if thehost == "mccr":
            my_OPSBIN='/home/mccronep/NEXRAD/python'
            #
        #----------------------

    #
    IS_THIS_ALPHA=0
    #
    #----------------------------------------------------------------
    if thehost == "a4au":
        #----------------------
        IS_THIS_ALPHA=1
        #----------------------
    #----------------------------------------------------------------
    #
    infromlinux = commands.getoutput('echo ${XFER_BASEPATH}')   ### XFER_BASEPATH=/satdat/curr/radar_nexrad_process
    #
    my_XFER_BASEPATH=infromlinux
    #
    #-----------------
    if my_XFER_BASEPATH== '':
        my_XFER_BASEPATH='/satdat/curr/radar_nexrad_process'
        #
    if thehost == "a4au":
        #----------------------
        #my_XFER_BASEPATH='/satdat/m4b/NEXRAD/NEXRAD_Display'
        my_XFER_BASEPATH='/satdat/curr/NEXRAD/NEXRAD_Display'
        my_XFER_BASEPATH='/satdat/curr/radar_nexrad_process'
        #
        #----------------------
    if thehost == "mccr":
        #my_XFER_BASEPATH='/home/mccronep/data'
        my_XFER_BASEPATH='/home/mccronep/data/m4b/NEXRAD'
        #
    #----------------------------------------------------
    #
    print("-------my-XFER-BASEBATH is: "+str(my_XFER_BASEPATH)+" -----------------")
    print(dadash+dadash)
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_XFER_BASEPATH)
    if (check_path == 0):
        print(dadash+dadash)
        print("This PATH is missing and it is a critical path. Ending program execution now.")
        print(dadash+dadash)
        this_execution=90
        #---------------------
        # END of IF Block
        #---------------------
    #
    #    
    #----------------------------------------------------
    #
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #
    infromlinux = commands.getoutput('echo ${RADAR_BASEPATH}')   
    ### RADAR_BASEPATH (should be)=/satdat/curr/NEXRAD/python/
    #
    my_RADAR_BASEPATH=infromlinux
    #
    #-----------------
    if my_RADAR_BASEPATH== '':
        my_RADAR_BASEPATH='/satdat/curr/NEXRAD/python/'
        #
    if thehost == "a4au":
        #----------------------
        my_RADAR_BASEPATH='/satdat/curr/NEXRAD/python/'
        #----------------------
    if thehost == "mccr":
        #----------------------
        ##my_RADAR_BASEPATH='/home/mccronep/data/m4b/NEXRAD/python/'
        my_RADAR_BASEPATH='/home/mccronep/python/src/NEXRAD/python/'
        #----------------------
        #
    #----------------------------------------------------
    #
    print("-------my-RADAR-BASEBATH is: "+str(my_RADAR_BASEPATH)+" -----------------")
    print(dadash+dadash)
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_RADAR_BASEPATH)
    if (check_path == 0):
        print(dadash+dadash)
        print("This PATH is missing and it is a critical path. Ending program execution now.")
        print(dadash+dadash)
        this_execution=90
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    JPEG_dir=my_RADAR_BASEPATH+'JPEG/'
    #
    GTIFF_dir=my_RADAR_BASEPATH+'GeoTIFF/'
    #
    the_files=1
    #
    linux_cmd='rm -rf '+JPEG_dir+'*.*'
    the_files=OS.system(linux_cmd)
    #
    if (the_files == 0):
        print('The files in the JPG directory were deleted successfully.')
    else:
        print('NOTICE: THE JPG FILE DELETIONs DID NOT OCCUR!!!')
        #---------------------
        # END of IF Block
        #---------------------
    #
    the_files=1
    #
    linux_cmd='rm -rf '+GTIFF_dir+'*.*'
    the_files=OS.system(linux_cmd)
    #
    if (the_files == 0):
        print('The files in the GeoTIFF directory were deleted successfully.')
    else:
        print('NOTICE: THE GeoTIFF FILE DELETIONs DID NOT OCCUR!!!')
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    #    
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #----------------------------------------------------------------
    #
    #----------------------------------------------------
    #
    # Decompress Level II data (Location of -C- binaries): 
    # /satdat/m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Decompress
    # == == == == == == == == == == == == == == == == == == ==
    #
    my_NEXRAD_decompress=my_XFER_BASEPATH+'/../NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Decompress/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_NEXRAD_decompress)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --my_NEXRAD_decompress--  : "+str(my_NEXRAD_decompress)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    # Convert Level II Binary data to ASCII (Location of -C- binaries):
    # /satdat/m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process
    # == == == == == == == == == == == == == == == == == == ==
    #
    #my_NEXRAD_ascii=my_XFER_BASEPATH+'/../../m4b/NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process/'
    my_NEXRAD_ascii=my_XFER_BASEPATH+'/../NEXRAD/NEXRAD_Display/NEXRAD_LVL2_Process/'
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_NEXRAD_ascii)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --my_NEXRAD_ascii--  : "+str(my_NEXRAD_ascii)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    # Display NEXRAD data as a graphic (Location of -IDL- source code):
    # /satdat/m4b/NEXRAD/NEXRAD_Display/NEXRAD_CompZ_IDL
    # == == == == == == == == == == == == == == == == == == ==
    #
    ##my_NEXRAD_IDL=my_XFER_BASEPATH+'/../../m4b/NEXRAD/NEXRAD_Display/NEXRAD_CompZ_IDL/'
    my_NEXRAD_IDL=my_XFER_BASEPATH+'/../NEXRAD/NEXRAD_Display/NEXRAD_CompZ_IDL/'
    #
    #
    check_path = 0
    check_path = IS_This_Path_Valid(my_NEXRAD_IDL)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The path --my_NEXRAD_IDL--  : "+str(my_NEXRAD_IDL)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #
    #----------------------------------------------------
    #----------------------------------------------------
    #
    alpha_sourcedatapath='/satdat/curr/m4b/radar/nexrad/'
    sourcedatapath='/u/curr/etc/dynamic/obs_data/met/cqc/radar/'
    #
    #
    if thehost == "a4au":
        sourcedatapath=alpha_sourcedatapath
        #
        #----------------------
    #
    check_path = 0
    check_path = IS_This_Path_Valid(sourcedatapath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The sourcedatapath: "+str(sourcedatapath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #----------------------------------------------------
    #----------------------------------------------------

    ##datarootpath=my_XFER_BASEPATH+'/../../m4b/NEXRAD/data/'
    datarootpath=my_XFER_BASEPATH+'/../NEXRAD/NEXRAD_Display/data/'

    #
    check_path = 0
    check_path = IS_This_Path_Valid(datarootpath)
    if (check_path == 0):
        print(dadash+dadash)
        print("ERROR: The datarootpath: "+str(datarootpath)+" is not valid. Please Check.")
        print(dadash+dadash)
        this_execution=90
        return this_execution
        #---------------------
        # END of IF Block
        #---------------------
    #
    #----------------------------------------------------
    #----------------------------------------------------
    #
    #

    for RADAR_Callsign in HIT_call_signs:
        #
        datapath=datarootpath+RADAR_Callsign+'/'
        #--
        #.....................
        #
        # Check datapath
        #

        check_path = 0
        check_path = IS_This_Path_Valid(datapath)
        if (check_path == 0):
            print(dadash+dadash)
            print("The stated path to RADAR site "+str(RADAR_Callsign)+" does not exist.")
            print("This PATH is missing. . Moving to the next RADAR SITE.")
            print(dadash+dadash)
            #this_execution=90
            #---------------------
            # END of IF Block
            #---------------------
        if (check_path == 1):
            print(dadash+dadash)
            print("The stated path to RADAR site "+str(RADAR_Callsign)+" EXISTS and IS GOOD.")
            print(dadash+dadash)
            #---------------------
            # END of IF Block
            #.....................
        #--
        #
        ##my_function_result = Decompress_NEXRAD_File(my_XFER_BASEPATH, RADAR_Callsign)
        if (check_path == 1):
            print('---BEGIN THE --PyART_NEXRAD_File-- FUNCTION  -----')
            #
            my_function_result = PyART_NEXRAD_File(sourcedatapath, datapath, my_XFER_BASEPATH, RADAR_Callsign, my_RADAR_BASEPATH)
            #
            print('---EXIT  THE --PyART_NEXRAD_File-- FUNCTION  -----')
            #
            #--------------------------------------------------------------
            #
            print('---BEGIN THE --PyART_NEXRAD_DopVel-- FUNCTION  -----')
            #
            my_function_result2 = PyART_NEXRAD_DopVel(sourcedatapath, datapath, my_XFER_BASEPATH, RADAR_Callsign, my_RADAR_BASEPATH)
            #
            print('---EXIT  THE --PyART_NEXRAD_DopVel-- FUNCTION  -----')
            #
            if (my_function_result == 77):
                check_path=0
                #
                print(dadash+dadash)
                print("No RAW Compressed data for RADAR Station :"+str(RADAR_Callsign)+" !! ")
                print("Skip to the next RADAR Station.  ")
                print(dadash+dadash)
                #------------------
        #
        #----------------------------------------------------
        #----------------------------------------------------
        #----------------------------------------------------
        #
        #
        #---------------------------------------------------------
        # END of -for- loop for RADAR_Callsign in HIT_call_signs: 
        #---------------------------------------------------------
        #
    #
    #----------------------------------------------------#--------------------------------------------
    #----------------------------------------------------#--------------------------------------------
    #----------------------------------------------------#--------------------------------------------
    #----------------------------------------------------#--------------------------------------------

    print('---ENDING THE --MAIN[]-- FUNCTION  -----')
    #
    print(dadash+dadash)

    print(dadash+dadash)
    #
    the_start_time = Print_Current_Time(right_now)
    print(" \n")
    print(dadash+dadash)
    print(dadash+dadash)
    #

    this_execution=1
    return this_execution
    ########################################################################################################
    ########################################################################################################
    #### END OF MAIN FUNCTION ##############################################################################
    ########################################################################################################
    ########################################################################################################
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
#
program_name="nexrad_image_process.py"
                                                                                             
print(dadash)
#print("-------Program BEGIN EXECUTION - {} -----------------").format(program_name)                                        
print("-------Program BEGIN EXECUTION - "+str(program_name)+" -----------------")
print(dadash)    

#
#----------------------------------------------------------------------
# This is the so-called primary part of the program where
# everything starts. It starts with invoking the -main- function below.
# The intent is to have virtually everything be done in the -main- function
# and call other functions as needed from within the -main- function.
# The reason for doing this is to enable error trapping more easily
# in the -main- routine. If the -main- code were not in a function, 
# then more effort would need to be expended in trapping runtime errors.
#
# For a simple demo of this idea , See: 
# http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html
#    
#----------------------------------------------------------------------
#

my_execution = 0

if WARNING_INIT_ERROR == 1:
    #
    my_execution=main()
    #
else:
    #
    my_execution = 11
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
#
#----------------------------------------------------------------
# Let me know if the program executed successfully.
# Otherwise, give me a --helpful-- error message!
#----------------------------------------------------------------

if my_execution == 1:
    print("--------------------------------------------------------------------------------")
    print("-------Program Executed SUCCESSFULLY, No Errors were detected! -----------------")
    print("--------------------------------------------------------------------------------")
    #
elif my_execution == 11:
    #
    print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    print("------Program Execution Code....."+str(my_execution))
    print("_________________________________________________________________________________")
    print("------There were or was an initialization error! A key configuration ------------")
    print("------file or files were either missing, or there was a permissions   -----------")
    print("------issue that prevented our ability to read the file or files.     -----------")
    print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    #
elif my_execution == 55:
    #
    print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    print("------Program Execution Code....."+str(my_execution))
    print("_________________________________________________________________________________")
    print("------There were or was no NETCDF file(s) available to be processed! ------------")
    print("------If there are no valid NETCDF files- the process just ends!  ---------------")
    print("------PLEASE CHECK PREVIOUS log entries for possible ERROR MESSAGES!!!!!!!! -----")
    print("------POSSILBE DPS or BFT problem! POSSIBLE SYSTEM OPERATING SYSTEM PROBLEM!-----")
    print("------POSSIBLE GPFS FILE SYSTEM PROBLEM!-----------------------------------------")
    print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    #
elif my_execution == 90:
    #
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    print("-------Program Execution Code....."+str(my_execution))
    print("_________________________________________________________________________________")
    print("-----There were or was a problem with PYTHON getting access to a PATH! ----------")
    print("-----In other words--- the software could not access a subdirectory it needs!  --")
    print("-----The software cant get to a data path either to read or write etc!  ---------")
    print("-----PLEASE CHECK PREVIOUS log entries for possible ERROR MESSAGES!!!!!!!! ------")
    print("-----POSSIBLE LINUX OPERATING SYSTEM PROBLEM! POSSIBLE GPFS FILE SYSTEM PROBLEM!-")
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    #
    #
elif my_execution == 97:
    #
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    print("-------Program Execution Code....."+str(my_execution))
    print("________________________________________________________________________________")
    print("-------Data conversion executed successfully (an ASCII file was made)....-------")
    print("-------but ....there were issues interfacing with the operating system! --------")
    print("-------Issues with the operating system could include......... -----------------")
    print("-------file copy- file move- file rename--- file permissions- etc.  ------------")
    print("-------PLEASE CHECK PREVIOUS log entries for possible ERROR MESSAGES!!!!! ------")
    print("-------POSSILBE DPS or DART problem! POSSIBLE SYSTEM OS PROBLEM!         -------")
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    #
else:
    #
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("-------Program Execution Code....."+str(my_execution))
    print("________________________________________________________________________________")
    print("-------It appears that the program did not execute properly!!!!!!!! ------------")
    print("-------The software exited with an unexpected error code!!!!!!!!!!! ------------")
    print("-------PLEASE CHECK PREVIOUS log entries for ERROR MESSAGES!!!!!!!! ------------")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    #-----------------------------------------------------------
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
#
#
#
##
#                                                                                             
#                                                                                             
#                                                                                             
#                                                                                             
print(dadash)                                                                                 
#print("-------Program END EXECUTION - {} -----------------").format(program_name)                                        
print("-------Program END EXECUTION - "+str(program_name)+" -----------------")
print(dadash)                                                                                 

#-------------------------------------------------------------------------------
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--## END OF PYTHON CODE                                                       
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
#                                                                               
#                               
