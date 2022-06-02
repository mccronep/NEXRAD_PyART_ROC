#! /bin/ksh
# SCCS IDENTIFICATION:  $HeadURL$
# SCCS IDENTIFICATION:  @(#)$Id$
#
#--------------------------------------------------------
#--------------------------------------------------------
#
# radar_nexrad_process_levelII.ksh
#
#--------------------------------------------------------
# Written by Paul McCrone
# Supports NEXRAD Level 2 data is processed 
#          as required to make RADAR Graphics.
#
# Version 1.4 DATED 2017-FEB-09
#
#--------------------------------------------------------
#--------------------------------------------------------
##xxxxxxxxx
#
# Define environment variables
#
typeset machine=$( uname -n )
typeset envir=$(echo $machine | cut -c 3-3 )
#
if [[ $envir == "d" || $envir == "a" ]]; then
   #typeset ROOTDATADIR=/satdat/m4b/NEXRAD/python/
   #typeset ROOTDATADIR=/satdat/curr/NEXRAD/python/
   typeset ROOTDATADIR=/satdat/bin/
   typeset LOGPATH=/satdat/curr/radar_nexrad_process/
fi
#
if [[ $envir == "b" || $envir == "o" ]]; then
   #typeset ROOTDATADIR=/satdat/m4b/NEXRAD/python/
   #typeset ROOTDATADIR=/satdat/curr/NEXRAD/python/
   typeset ROOTDATADIR=/u/curr/bin/
   typeset LOGPATH=/satdat/curr/radar_nexrad_process/
fi
#

JDAY=$(date +%j)

DDMMYY=$(date +%F)

HH=$(date +%H)

MM=$(date +%M)

##LOGPATH=/satdat/m4b/NEXRAD/python/


#LOGFILE=${LOGPATH}runner_nexrad.log.log
LOGFILE=${LOGPATH}log.runner_Py_nexrad_log

#runner_Py_nexrad.log.log


DASHES=----------------------------------------------------

echo ${DASHES} >> ${LOGFILE}
date           >> ${LOGFILE}
echo ${DASHES} >> ${LOGFILE}

cd ${ROOTDATADIR}

${ROOTDATADIR}run_Py_nexrad.ksh >> ${LOGFILE}

echo ${DASHES} >> ${LOGFILE}

rm ${XFER_BASEPATH}/radar_nexrad_process*.init.dat


##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##  END OF radar_nexrad_process_levelII.ksh
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
