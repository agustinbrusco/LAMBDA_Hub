#!/bin/bash

Vvsub=70  # V: Tensión de sustrato a 70 V post limpiar

imgFOLDER=`dirname $BASH_SOURCE`/images/TRAPS/13NOV2023_150K
#runname=cleanning
exposure_time=8.0
lightoledaxis='row'  # A col in OLED is horizontal at CCD screen
runname=pocket_oled1${lightoledaxis}_2film

lockfilename=lockfile  # kind of an Env Var


doClean(){
    lta CCDNROW 1658
    lta CCDNCOL 572
	lta NROW 829
	lta NCOL 336
	lta NSAMP 1
	lta EXPOSURE 0
	lta name $imgFOLDER/skp_${runname}_NSAMP1_NROW829_NCOL336_EXPOSURE0_cleanimg
	lta read
	}

doSettings(){
    lta CCDNROW 1658
    lta CCDNCOL 572
    rows=879
	lta NROW $rows
    cols=336
	lta NCOL $cols
    nsmpls=100
	lta NSAMP $nsmpls
    expo=0
	lta EXPOSURE $expo
    npumps=40000
    lta NPUMPS $npumps
	}

touch $lockfilename
mkdir -p $imgFOLDER

source init_mit.sh

source voltages/voltage_skp_lta_v2_C_safe.sh  # Preguntar!
#source voltages/voltage_skp_lta_v2_microchip.sh  # Recomendación Santi

source eraseANDepurge.sh
lta set vsub $Vvsub

doClean
doClean
doClean

#for dtph in 50 100 200 400 800 1600 3200 6400 12800 25600 51200 102400 204800 409600 819200 1638400 3276800
for dtph in 50 100 200 400 800 1600 3200
#for dtph in 3200 6400 12800 25600 51200 102400 204800 409600 819200 1638400 3276800
do
    if [ ! -f "$lockfilename" ]; then break; fi
        lta sseq sequencers/sequencer_microchip_binned_brenda.xml
	doClean

        lta sseq sequencers/sequencer_microchip_ppump.xml
        doSettings
        lta delay_Tph $dtph

        python minilambda_oled_connection.py $lightoledaxis $exposure_time
        sleep $exposure_time

        lta name $imgFOLDER/skp_${runname}_dTph${dtph}_NPUPMPS${npumps}_NSAMP${nsmpls}_NROW${rows}_NCOL${cols}_EXPOSURE${exposure_time}_img
        lta read
done
