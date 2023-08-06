# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:54:18 2013

@author: odile32
"""


# carriage return string
# for unix
# cr_string = "\r\n"

# for windows
cr_string = "\n"

omega_sample_frame = 40.0

from math import cos, sin, pi
import numpy as np

if omega_sample_frame != None:
    omega = omega_sample_frame * pi / 180.0
    # rotation de -omega autour de l'axe x pour repasser dans Rsample
    mat_from_lab_to_sample_frame = np.array([[1.0, 0.0, 0.0],
                                            [0.0, cos(omega), sin(omega)],
                                            [0.0, -sin(omega), cos(omega)]])
else:
    mat_from_lab_to_sample_frame = np.eye(3)  # put

add_str_fitfile = "_t_UWN_mg"

add_str_datfile = ""

# invisible parameters for serial_peak_search


# attention les analyses avant le 29/10/2013
# utilisaient pixelsize = 165/2048 (au lieu de 0.07914 mm) pour MARCCD165
# analyses correctes mais pas avec le bon dd

CCDlabel = "MARCCD165"
# CCDlabel = "ROPER159"   # OK for ROPER except few experiments Jul11-Sep11
# voir dict_CCD dans dict_LaueTools.py pour la liste des cameras / orientations de cameras

number_of_digits_in_image_name = 4

LT_REV_peak_search = "1168"  # LaueTools revision - for info only

overwrite_peak_search = 1

local_maxima_search_method = 2

thresholdConvolve = 900

CDTE, GE, W, C_VHR_May12, C_VHR_Nov12, NOFIT, SI_VHR_Feb13, CU = 1, 0, 0, 0, 0, 0, 0, 0

if CDTE:
    PixelNearRadius = 10
    IntensityThreshold = 100
    boxsize = 5
    position_definition = 1
    fit_peaks_gaussian = 1
    xtol = 0.001
    FitPixelDev = 2.0
    local_maxima_search_method = 1

if CU:  # Dec09
    PixelNearRadius = 10
    # IntensityThreshold = 250
    IntensityThreshold = 300
    boxsize = 10
    position_definition = 1
    fit_peaks_gaussian = 1
    xtol = 0.001
    FitPixelDev = 5.0

if NOFIT:

    PixelNearRadius = 10
    # IntensityThreshold = 500
    IntensityThreshold = 300
    boxsize = 5
    # XMAS offset
    position_definition = 1
    fit_peaks_gaussian = 0
    xtol = 0.001
    # FitPixelDev = 0.7
    FitPixelDev = 2.0

if GE:
    PixelNearRadius = 10
    # IntensityThreshold = 500
    IntensityThreshold = 300
    boxsize = 5
    # XMAS offset
    position_definition = 1
    fit_peaks_gaussian = 1
    xtol = 0.001
    # FitPixelDev = 0.7
    FitPixelDev = 2.0

if W:  # Sep08
    PixelNearRadius = 5
    # IntensityThreshold = 250
    IntensityThreshold = 300
    boxsize = 5
    position_definition = 1
    fit_peaks_gaussian = 1
    xtol = 0.001
    FitPixelDev = 2.0

if C_VHR_May12:
    #             'VHR_diamond':((2594, 3764), 0.031, 4095, "vhr", 4096, "uint16",
    #                            "first vhr settings of Jun 12 close to diamond 2theta axis displayed is vertical, still problem with fit from PeakSearchGUI", "tiff"),
    CCD_label = "VHR_diamond"
    local_maxima_search_method = 0
    PixelNearRadius = 100
    # IntensityThreshold = 250
    IntensityThreshold = 300
    boxsize = 20
    position_definition = 1
    fit_peaks_gaussian = 1
    xtol = 0.001
    FitPixelDev = 25.0

if C_VHR_Nov12:
    #                 'VHR_small':((2594, 2748), 0.031, 4095, "vhr", 4096, "uint16",
    #                          "vhr close to diamond Nov12 frame size is lower than VHR_diamond", "tiff"),
    CCD_label = "VHR_small"
    # basic method
    local_maxima_search_method = 0
    PixelNearRadius = 100
    IntensityThreshold = 190
    # IntensityThreshold = 300
    boxsize = 20
    position_definition = 1
    fit_peaks_gaussian = 0
    xtol = 0.001
    FitPixelDev = 25.0


if SI_VHR_Feb13:  # VHR for sample
    #             'VHR_Feb13':((2594, 2774), 0.031, 4095, 'VHR_Feb13', 4096, "uint16",
    #                          "vhr settings of Feb13 close to sample 2theta axis displayed is vertical, no problem with fit from PeakSearchGUI", "tiff"),

    # TODO : rajouter if res == 0 pour si en dehors de l'echantillon
    CCDlabel = "VHR_Feb13"
    local_maxima_search_method = 2
    PixelNearRadius = 20
    IntensityThreshold = 20.0
    boxsize = 30
    position_definition = 1
    fit_peaks_gaussian = 1
    xtol = 0.001
    FitPixelDev = 25.0
    thresholdConvolve = 2050

# invisible parameters for
# index_refine_multigrain_one_image
# serial_index_refine_multigrain
# index_refine_calib_one_image
# serial_index_refine_calib

filter_peaks_index_refine_calib = 1

maxpixdev_filter_peaks_index_refine_calib = 0.7

elem_label_index_refine_calib = "Ge"

elem_label_index_refine = "CdTe"
# voir dict_Materials dans dict_LaueTools.py pour la liste des structures cristallines
# pas besoin de parametres de maille tres precis sauf si mesures de Espot

# ngrains_index_refine = 4  # try to index up to "ngrains_index_refine" grains

ngrains_index_refine = (
    1
)  # try to index up to "ngrains_index_refine" grains , version avec proposed_matrix

overwrite_index_refine = 1  # overwrite existing fit files

add_str_index_refine = "_t_UWN_mg"  # string to add : UWN = "use weights no"

# invisible parameters in index_refine_one_image

check_grain_presence = None

remove_sat_calib = 0
elim_worst_pixdev_calib = 1
maxpixdev_calib = 1.0
spot_index_central_calib = 0
nbmax_probed_calib = 10
energy_max_calib = 23
rough_tolangle_calib = 0.5
fine_tolangle_calib = 1.0
Nb_criterium_calib = 20
NBRP_calib = 1


A16DEC13 = 1

if A16DEC13:

    remove_sat = 0
    elim_worst_pixdev = 1
    maxpixdev = 7.0
    energy_max = 22
    fine_tolangle = 0.4
    Nb_criterium = 20

A21DEC13 = 0

if A21DEC13:

    remove_sat = 0
    elim_worst_pixdev = 1
    maxpixdev = 1.5
    energy_max = 22
    fine_tolangle = 0.3
    Nb_criterium = 20
    check_grain_presence = None

# check_grain_presence = 1

# remove_sat=0  # remove saturated spots with Ipixmax = Saturation value defined by CCDlabel
# = 1 : keep saturated peaks (Ipixmax = saturation vaue) for indexation but remove them for refinement

# elim_worst_pixdev=1 # after first strain refinement, eliminate spots with pixdev > maxpixdev
# only one iteration i.e. sometimes a few spots with pixdev > maxpixdev remain
#
# maxpixdev=4.5

spot_index_central = [
    0
]  # 1,2]  # spot(s) used a first spot when testing doublets for indexation
#    spot_index_central = [0,1,2,3,4,5]  # central spot or list of spots

nbmax_probed = 10  #     # 'Recognition spots set Size (RSSS): '
# number of spots to be used as second spot when testing doublets for indexation
# selected spots = first nbmax_probed spots from spotlist
# spots in spotlist are sorted according to decreasing intensity

# energy_max=22 # keV

rough_tolangle = (
    0.5
)  #    # 'Dist. Recogn. Tol. Angle (deg)'      # for testing doublets

# fine_tolangle=0.2 #   # 'Matching Tolerance Angle (deg)'       # for spotlink exp - theor
# pour analyse multigrain

# fine_tolangle=0.2 #   # 'Matching Tolerance Angle (deg)'       # for spotlink exp - theor
# pour analyse monograin avec proposed_matrix
# bug : en fait verycloseangletol fixe a 0.1 dans test_index_refine
# pour toutes les analyses avec proposed_matrix != None et paramtofit = strain avant 24Jul13
# bug corrige le 24Jul13
# fitfiles2b / G0 utilise fine_tolangle = 0.2

# fine_tolangle = 0.4 # apres correction 04Nov13 du bug check_grain_presence = 0 au lieu de None

# Nb_criterium=20, #   # 'Minimum Number Matched Spots: '

NBRP = 1  #    NBRP = 1 # number of best result for each element of spot_index_central

mark_bad_spots = 1
#      mark_bad_spots = 1 : for multigrain indexation, at step n+1 eliminate from the starting set all the spots
#                              more intense than the most intense indexed spot of step n
#                              (trying to exclude "grouped intense spots" from starting set)


# parameters for get_xyzech

xech_offset = 0xE00
yech_offset = 0xE07
zech_offset = 0xE0E

# TODO : rajouter mon_offset

# parameters for build_summary

nbtopspots = (
    10
)  # mean local grain intensity is taken over the most intense ntopspots spots

# parameters for add_columns_to_summary_file

filestf = "CdTe.stf"

# parameters for class_data_into_grainnum
# drgb = 0.03 donne approximativement desorientation = 0.15 deg

# rgb_tol_class_grains = 0.03


# parameters for plot_all_grain_maps

# map_rotation = 90.  # article et chap
map_rotation = 0.0


# dummy values for variables
# to be updated in multigrain
# when calling init_vectors_for_orientation_color_calculation
# goal : avoid recalculating the variables at each call of matstarlab_to_orientation_color_rgb

cos0 = 0.0
cos1 = 0.0
cos2 = 0.0

from numpy import zeros

uqn_r = zeros(3, float)
uqn_b = zeros(3, float)
uqn_g = zeros(3, float)

uqref_cr = zeros((3, 3), float)
#

struct1 = None
nop = None
indgoodop = None
