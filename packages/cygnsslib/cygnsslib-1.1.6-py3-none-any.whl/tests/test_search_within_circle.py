#!/usr/bin/env python3

#  FILE     TBD
#  DESCRIPTION
#           TBD
#  AUTHOR   James D. Campbell
#           Microwave Systems, Sensors and Imaging Lab (MiXiL)
#           University of Southern California
#  EMAIL    jamesdca@usc.edu
#  CREATED  2018-12-12
#
#  Copyright 2018 University of Southern California

import cygnsslib
import os


cygnss_l1_path = os.environ["CYGNSS_L1_PATH"]
year = [2019]

daylist = list(range(1, 30))

radius = 5e3
thesh_ddm_snr = 3
thesh_noise = 1
out_root = 'yanco_2019'
ref_pos = [-34.856660, 146.140752]  # Yonco
out_high, out_low, out_ref = cygnsslib.write_sp_within_radius(cygnss_l1_path, year, daylist, ref_pos, radius, out_root, thesh_ddm_snr, thesh_noise)

out_kml = 'grp1_{:s}'.format(out_high)
cygnsslib.group_sp_within_distance(out_high, out_kml=out_kml, max_dist=100, save_cvs=True)
