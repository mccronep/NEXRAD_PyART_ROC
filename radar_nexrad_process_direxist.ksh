#! /bin/ksh
#
# --------------------
# radar_nexrad_process
# --------------------
#
#----------------------------------
# SCCS IDENTIFICATION:  $HeadURL$
# SCCS IDENTIFICATION:  @(#)$Id$
# Programmer, Paul McCrone, N38DI
#             x1503
#             January 5, 2016
#----------------------------------
#
#------------------------------------------------------------------------------
####    --radar_nexrad_process_direxist.ksh--
####
####    Functions for an PBS task that processes the NEXRAD LevelII data for
####    coverting the NEXRAD LevelII files to graphics [jpg] data
####
####    This script will check for the existence of key
####    subdirectories needed by radar_nexrad_process and will
####    re-create the subdirectories if they do not exist.
####
####
#------------------------------------------------------------------------------
#
# Version A.1.0, 2016-Dec-10 
#
#------------------------------------------------------------------------------

#### RECORD OF CHANGES:
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#
#    January 5, 2017  Paul McCrone, x1503 Release Version VA.1.0
#
#
#------------------------------------------------------------------------------
#
#################################################
#
#--------------------------
date
echo ..........The Script -radar_nexrad_process_direxist.ksh- BEGINS:
echo ---------------------------------------------------------------------

#--------------------------
#--------------------------
#--------------------------
#
# Define environment variables
#
#

typeset ENDINGF=_alpha_

typeset machine=$( uname -n )
typeset envir=$(echo $machine | cut -c 3-3 )
typeset THISHOSTNAME=$(echo $machine | cut -c 1-4)

#
if [[ $envir == "d" || $envir == "a" ]]; then
   typeset ENDINGF=_alpha_
fi
#
if [[ $envir == "b" || $envir == "B" ]]; then
   typeset ENDINGF=_beta_
fi
#
if [[ $THISHOSTNAME == "a4ou" ]]; then
   typeset ENDINGF=_OPS_
fi
#
#
#--------------------------
#--------------------------
#--------------------------

echo --
echo --
echo --

echo Running_on_HOSTNAME_${THISHOSTNAME}
echo Current_Running_Environment_is_${ENDINGF}


echo --
echo --
echo --

###--export OPSPATH=/satdat
###--export OPSBIN=$OPSPATH/bin
###--export OPSFCN=$OPSPATH/job/bin
###--export XFER_BASEPATH=/satdat/alpha/rscat_knmi

export BETAPATH=/u/beta

#=============================================================
if [[ -d ${OPSPATH} && -n${OPSPATH} ]]
then
        echo OPSPATH_EXISTS_AND_IS_${OPSPATH}._
else
        echo OPSPATH_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export OPSPATH=/satdat
        if [[ $envir == "b" || $envir == "B" ]]; then
           export OPSPATH=/u/curr
        fi
        if [[ $THISHOSTNAME == "a4ou" ]]; then
           export OPSPATH=/u/curr
        fi
        echo OPSPATH_IS_NOW_${OPSPATH}_.
fi
#=============================================================
if [[ -d ${OPSBIN} && -n${OPSBIN} ]]
then
        echo OPSBIN_EXISTS_AND_IS_${OPSBIN}._
        if  [[ $envir == "d" || $envir == "a" ]]
        then
                export OPSBIN=/satdat/bin
                echo FOR_ALPHA_ONLY--OPSBIN_EXISTS_AND_IS_RESET_TO__${OPSBIN}_.
        fi
else
        echo OPSBIN_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export OPSBIN=$OPSPATH/bin
        if  [[ $envir == "d" || $envir == "a" ]] 
        then
        	export OPSBIN=/satdat/bin 
        fi
        echo OPSBIN_IS_NOW_${OPSBIN}_.
fi
#=============================================================
if [[ -d ${OPSFCN} && -n${OPSFCN} ]]
then
        echo OPSFCN_EXISTS_AND_IS_${OPSFCN}._
else
        echo OPSFCN_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export OPSFCN=$OPSPATH/job/bin
        echo OPSFCN_IS_NOW_${OPSFCN}_.
fi
#=============================================================
if [[ -d ${XFER_BASEPATH} && -n ${XFER_BASEPATH} ]]
then
        echo ${XFER_BASEPATH}_EXISTS
else
        echo XFER_BASEPATH_NOT_AVAILABLE._WE_WILL_REASSIGN.
        export XFER_BASEPATH=/satdat/curr/radar_nexrad_process
        echo XFER_BASEPATH_IS_NOW_${XFER_BASEPATH}_.
fi
#=============================================================

#
export RSCAT_BASEPATH=$XFER_BASEPATH/../NEXRAD
#
export KNMI_BASEPATH=$RSCAT_BASEPATH/NEXRAD_Display/data
#
RADAR_BASEPATH=$RSCAT_BASEPATH/python/
#
#
GRAPHICPATH=$RSCAT_BASEPATH/python/JPEG/
#

##DATAPATH=/satdat/curr/rscat_knmi/
DATAPATH=$XFER_BASEPATH/
#
##BINPATH=/u/ops/bin/
BINPATH=$OPSBIN/
#
UTILPATH=$KNMI_BASEPATH/Nutil/
#
PROCPATH=$KNMI_BASEPATH/Nprocessed/
#

#=============================================================


if [ -d ${GRAPHICPATH} ]
then
        echo ${GRAPHICPATH}_EXISTS
else
        echo ${GRAPHICPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        #cd /satdat/curr/RapidScat/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir graphic
fi

#=============================================================

#=============================================================

if [ -d ${DATAPATH} ]
then
        echo ${DATAPATH}_EXISTS
else
        echo ${DATAPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/
        cd $XFER_BASEPATH/..
        mkdir radar_nexrad_process
fi

#=============================================================
###
###if [ -d ${BINPATH} ]
###then
###        echo ${BINPATH}_EXISTS
###else
###        echo ${BINPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
###        cd /satdat/curr/RapidScat/KNMI/
###        mkdir ascii_temp
###fi
###
#=============================================================

if [ -d ${UTILPATH} ]
then
        echo ${UTILPATH}_EXISTS
else
        echo ${UTILPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir Nutil
fi

#=============================================================

if [ -d ${PROCPATH} ]
then
        echo ${PROCPATH}_EXISTS
else
        echo ${PROCPATH}_NOT_AVAILABLE._PLEASE_RECREATE.
        ##cd /satdat/curr/RapidScat/KNMI/
        cd ${KNMI_BASEPATH}/
        mkdir Nprocessed
fi

#=============================================================

echo --
echo --
echo --

#--------------------------
echo ---------------------------------------------------------------------
echo ..........The Script -rscat_knmi_direxist.ksh- ENDS:
date
echo ---------------------------------------------------------------------
#--------------------------

#
################################################
######   END
################################################

