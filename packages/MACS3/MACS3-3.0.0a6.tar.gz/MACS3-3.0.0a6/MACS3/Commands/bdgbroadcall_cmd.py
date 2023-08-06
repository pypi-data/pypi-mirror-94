# Time-stamp: <2020-12-03 14:26:29 Tao Liu>

"""Description: Fine-tuning script to call broad peaks from a single
bedGraph track for scores.

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).

"""

# ------------------------------------
# python modules
# ------------------------------------

import sys
import os
import logging
from MACS3.IO import BedGraphIO
# ------------------------------------
# constants
# ------------------------------------
logging.basicConfig(level=20,
                    format='%(levelname)-5s @ %(asctime)s: %(message)s ',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    stream=sys.stderr,
                    filemode="w"
                    )

# ------------------------------------
# Misc functions
# ------------------------------------
error   = logging.critical		# function alias
warn    = logging.warning
debug   = logging.debug
info    = logging.info
# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main function
# ------------------------------------
def run( options ):
    info("Read and build bedGraph...")
    bio = BedGraphIO.bedGraphIO(options.ifile)
    btrack = bio.build_bdgtrack(baseline_value=0)

    info("Call peaks from bedGraph...")

    bpeaks = btrack.call_broadpeaks (options.cutoffpeak, options.cutofflink, options.minlen, options.lvl1maxgap, options.lvl2maxgap)

    info("Write peaks...")

    if options.ofile:
        bf = open( os.path.join( options.outdir, options.ofile ), "w" )
        options.oprefix = options.ofile
    else:
        bf = open ( os.path.join( options.outdir, "%s_c%.1f_C%.2f_l%d_g%d_G%d_broad.bed12" % (options.oprefix,options.cutoffpeak,options.cutofflink,options.minlen,options.lvl1maxgap,options.lvl2maxgap)), "w" )
    bpeaks.write_to_gappedPeak(bf, name_prefix=(options.oprefix+"_broadRegion").encode(), score_column="score", trackline=options.trackline)
    info("Done")
