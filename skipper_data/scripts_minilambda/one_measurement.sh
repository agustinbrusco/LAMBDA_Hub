#!/bin/bash

Vvsub=70  # V: Tensión de sustrato a 70 V post limpiar

imgFOLDER=`dirname $BASH_SOURCE`/images/TRAPS/15SEP2023
runname=no_cover_shutter_calibration

lockfilename=lockfile  # kind of an Env Var

doClean(){
        if [ ! -f "$lockfilename" ]; then break; fi
	lta NROW 829
	lta NCOL 336
	lta NSAMP 1
	lta EXPOSURE 0
	lta name $imgFOLDER/skp_${runname}_NSAMP1_NROW829_NCOL336_EXPOSURE0_cleanimg
	lta read
	}

doSettings(){
	rows=20  #829
	lta NROW $rows
    cols=336
	lta NCOL $cols
    nsmpls=400
	lta NSAMP $nsmpls
    expo=0
	lta EXPOSURE $expo
	}

touch $lockfilename
mkdir -p $imgFOLDER

source init_mit.sh

source voltages/voltage_skp_lta_v2_C_safe.sh

source eraseANDepurge.sh
lta set vsub $Vvsub

doClean
doClean
doClean
doClean

doSettings
lta name $imgFOLDER/skp_${runname}_NSAMP${nsmpls}_NROW${rows}_NCOL${cols}_EXPOSURE${exposure_time}_img
lta read