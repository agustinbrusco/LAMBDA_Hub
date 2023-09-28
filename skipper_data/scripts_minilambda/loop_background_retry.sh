#!/bin/bash

Vvsub=70  # V: Tensión de sustrato a 70 V post limpiar

imgFOLDER=`dirname $BASH_SOURCE`/images/TRAPS/28SEP2023
runname=no_cover_shutter_calibration

lockfilename=lockfile  # kind of an Env Var

doClean(){
	lta NROW 829
	lta NCOL 336
	lta NSAMP 1
	lta EXPOSURE 0
	lta name $imgFOLDER/skp_${runname}_NSAMP1_NROW829_NCOL336_EXPOSURE0_cleanimg
	lta read
	}

doSettings(){
	rows=829
	lta NROW $rows
    	cols=336
	lta NCOL $cols
    	nsmpls=1
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
# doClean  # fourth doClean inside loop

for i in 1 2 3 4 5 6 7 8 9 10
do
    for exposure_time in 300 600 900 1200 1500 1800 # seconds
    do
		# the while loop repeats the measurement until it's succesful
		# a measurement is succesful if no .dat symbolic links have been created at the end of the loop
		succes_read=false
		while [ $succes_read = false ]
		do
            if [ ! -f "$lockfilename" ]; then break; fi

            doClean
            sleep $exposure_time

            doSettings
            lta name $imgFOLDER/skp_${runname}_NSAMP${nsmpls}_NROW${rows}_NCOL${cols}_EXPOSURE${exposure_time}_img
            lta read
			if [[ $(ls $imgFOLDER | grep -c .dat$) -eq 0 ]]; then
				succes_read=true
			else
				rm $imgFOLDER/*.dat
			fi
		done
    done
done
