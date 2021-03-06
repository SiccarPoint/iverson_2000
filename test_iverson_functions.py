# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 09:22:28 2016

@author: smudd
"""

from __future__ import print_function
import Iverson_funcs as IvF
import iverson_2000 as I2000
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as patches


label_size = 8
axis_size = 12

# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = label_size
rcParams['xtick.major.size'] = 4
rcParams['ytick.major.size'] = 4
rcParams['legend.fontsize'] = label_size
rcParams['legend.handletextpad'] = 0.05
rcParams['legend.labelspacing'] = 0.1
rcParams['legend.columnspacing'] = 0.1

def test_FoS():

    # These are some characteristics of the slope. they come from the Minor Creek Landslide
    alpha = math.radians(15.)
    friction_angle = math.radians(18)

    # Here are the rainfall intensities
    Iz_over_Kz_steady = 0.1     # intensity of "steady state" pressure profile
    Iz_over_Kz = 1              # intensity of storm event

    # set up the spatial coordinates
    Zs = np.linspace(0.01, 6., 10)
    #Z = 0.01
    beta = IvF.Beta_fn(alpha, Iz_over_Kz_steady)
    
    # set up the weight of soil and water (this is density times gravity in SI units, see Iverson table 2)
    weight_of_soil = 22000
    weight_of_water = 9800
    
    # Cohesion in Pa
    cohesion = 4000
    
    # calculate the Factor of safety contribution from friction
    F_f = IvF.F_f(alpha, friction_angle)
    print("F_f is: " + str(F_f))
    
    # Calculate the factor of safety contribution from cohesion
    F_c = IvF.F_c(cohesion, weight_of_soil, Zs, alpha)
    print("F_c is: ")
    print(F_c) 


    # Now calculate the Factor of safety from water
    t = 24
    T = 12
    d = 2
    t_sec = IvF.weeks_to_secs(t)
    T_sec = IvF.weeks_to_secs(T)
    Do = 0.000001
    D_hat = IvF.D_hat_fn(Do, alpha)

    # First calculate Psi
    print("Z is: ")
    print(Zs)
    print("Now hold on a sec while I calculate pressure")
    this_psi = IvF.psi_dimensional_t(Zs, beta, d, Iz_over_Kz, D_hat, t_sec, T_sec)
    
    print("The psi values are: ")
    print(this_psi)

    # Correct Pis: it is limited by the beta curve (which is just the saturated pore pressure)    
    corr_psi = IvF.Correct_psi(Zs,this_psi,beta)
    print("The corrected psi values are:")
    print(corr_psi)
    
    # Now get the FoS contribution from the pore pressure
    F_w = IvF.F_w(corr_psi, weight_of_water, weight_of_soil, alpha, friction_angle, Zs)
    print("F_w is: ")
    print(F_w) 
    
    # Now get the Factor of safety
    FS = IvF.FS(corr_psi, weight_of_water, weight_of_soil, alpha, cohesion, friction_angle, Zs)
    print("FS is:")
    print(FS)
    
    # Now for the plots
    t_weeks = [0, 4, 8, 12, 24]
    t_sec = IvF.weeks_to_secs(t_weeks)
    name_string = "Figure10.png"

    IvF.Iverson_FoS_Fig10(weight_of_water, weight_of_soil, alpha, cohesion, friction_angle, d, Iz_over_Kz, Iz_over_Kz_steady, Do, t_sec, T_sec,name_string)
    
    
    # lets do figure 11
    weight_of_water = 9800
    weight_of_soil = 19000
    alpha = math.radians(31)
    cohesion = 500
    friction_angle = math.radians(38)
    d = 0.7
    Iz_over_Kz  = 1
    Iz_over_Kz_steady = 0
    Do = 0.001
    
    T_minutes = 10
    T_sec = IvF.minutes_to_secs(T_minutes)         
    t_minutes = [0,2,6,10,20]       
    t_sec = IvF.minutes_to_secs(t_minutes) 
    name_string = "Figure11.png"
    
    IvF.Iverson_FoS_Fig11(weight_of_water, weight_of_soil, alpha, cohesion, friction_angle, d, Iz_over_Kz, Iz_over_Kz_steady, Do, t_sec, T_sec,name_string)

def compare_linear_to_loop():

    t_stars = np.linspace(0.2, 10000, 15)

    print("t_stars are:")
    print(t_stars)

    vals = []
    vals2 = []

    for t in t_stars:
        vals.append(I2000.R_fn(t))
        vals2.append(IvF.R_fn(t))

    R = IvF.R_fn(t_stars)

    print("Version 1: ")
    print(vals)

    print("Version 2: ")
    print(R)

    print("Version 3: ")
    print(vals2)

    R2 = IvF.R_fn(0.1)
    print("R2 is")
    print(R2)

    R2 = IvF.R_fn(0.0001)
    print("R2 is")
    print(R2)
    
    # These are some characteristics of the slope
    alpha = math.radians(15.)

    # Here are the rainfall intensities
    Iz_over_Kz_steady = 0.1     # intensity of "steady state" pressure profile
    Iz_over_Kz = 1              # intensity of storm event

    # set up the spatial coordinates
    Z = np.linspace(0.0, 6., 13)
    beta = IvF.Beta_fn(alpha, Iz_over_Kz_steady)

    # ==========================================================
    # test the part of the function that calculates pressure
    print("beta is: ")
    print(beta)

    t_star = 0.0001
    T_star = 10

    # This is the depth of the steady state water table
    d = 2

    Z = 2.3

    # Test the pressure function. This solves equations 27a and b
    this_psi = IvF.psi(Z, beta, d, Iz_over_Kz, t_star, T_star)
    print("This Z is: ")
    print(Z)
    print("This psi is: ")
    print(this_psi)
    # ===========================================================

    # time and peak time of rainfall duration are in weeks so we need to
    # convert them to seconds
    t = 2
    T = 10
    t_sec = IvF.weeks_to_secs(t)
    T_sec = IvF.weeks_to_secs(T)
    Do = 0.000001
    D_hat = IvF.D_hat_fn(Do, alpha)

    Zs = np.linspace(0.01, 6., 10)
    print("Z is: ")
    print(Zs)
    print("Now hold on a sec while I calculate pressure")
    this_psi = IvF.psi_dimensional_t(Zs, beta, d, Iz_over_Kz, D_hat, t, T)

    print("And now for the dimensional psi: ")
    print(this_psi)

    # reset the t variable for the figure
    t = [0, 4, 8, 12, 24]

    # calculate figure 7
    print("I am making figure 7b")
    IvF.Iverson_Fig_7(t, T, d, Do, alpha, Iz_over_Kz, Iz_over_Kz_steady)

    print("Okay now I am going to do figure 7a")
    # now do the other one
    fig7a_ts = [0, 2, 6, 10, 20]
    t = IvF.days_to_weeks(fig7a_ts)
    fig_7a_T = 10
    T = IvF.days_to_weeks(fig_7a_T)
    IvF.Iverson_Fig_7(t, T, d, Do, alpha, Iz_over_Kz, Iz_over_Kz_steady)


def test_time_series():

    # These are some characteristics of the slope. they come from the Minor Creek Landslide
    alpha = math.radians(15.)
    print("alpha is: "+str(alpha))    
    
    friction_angle = math.radians(18)

    # Here are the rainfall intensities
    Iz_over_Kz_steady = 0.1     # intensity of "steady state" pressure profile
    Intensities = [0.5,1,0.5]              # intensity of storm events
    Durations = [5,6,4]               # durations of the events

    # set up the spatial coordinates
    Zs = np.linspace(0.01, 6., 10)
    
    print("Depths are: ")
    print(Zs)    
    #Z = 0.01
    beta = IvF.Beta_fn(alpha, Iz_over_Kz_steady)
    

    # Now calculate the Factor of safety from water
    t = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    d = 2
    #t_sec = IvF.weeks_to_secs(t)
    durations_sec = IvF.weeks_to_secs(Durations)
    Do = 0.000001
    D_hat = IvF.D_hat_fn(Do, alpha)

    ts = IvF.weeks_to_secs(11)
    print("ts is: "+str(ts))
    psi = IvF.psi_dimensional_from_time_series(durations_sec,Intensities,Zs, beta, d, D_hat, ts)
    
    print("durations_sec:")
    print(durations_sec)       
    
    print("Psi is:")
    print(psi)

    weight_of_water = 9800
    weight_of_soil = 19000
    #alpha = math.radians(31)
    cohesion = 500
    friction_angle = math.radians(38)
    print("Alpha: "+str(alpha)+ " and friction_angle: "+str(friction_angle))
    FS = IvF.FS(psi, weight_of_water, weight_of_soil, alpha, cohesion, friction_angle, Zs)
    print("The factor of safety is: ")
    print(FS)
    
    

'''
    Fig1 = plt.figure(1, facecolor='white', figsize=(10, 8))

    Fig1.gca().invert_yaxis()
    count = 0
    for t_week in t:
        ts = IvF.weeks_to_secs(t_week)
        this_label = 't = ' + str(t_week) + ' weeks'
        psi = IvF.psi_dimensional_from_time_series(durations_sec,Intensities,Zs, beta, d, D_hat, ts)
        plt.plot(psi, Zs, label=this_label)
        count = count+1
        legend = plt.legend()
        legend.get_frame().set_linewidth(0.)
        plt.xlabel('Pressure head (m)')
        plt.ylabel('Depth (m)')
        plt.title('Transient')
        plt.xlim(-2, 5)
        plt.tight_layout()

        plt.savefig("Test_transient"+str(100+count)+".png", format="png")

        plt.cla()

    # 

    #plt.show()
'''

if __name__ == "__main__":
    #compare_linear_to_loop()
    #test_FoS()
    test_time_series()