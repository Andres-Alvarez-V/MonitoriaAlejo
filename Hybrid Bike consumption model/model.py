# ============ Main code ===========================
# This code execute the dynamic model for HEM
def bike_model(init_soc, hybrid_cont):
    from parameters import HEV
    import numpy as np
    import math
    #import time
    import matplotlib.pyplot as plt
    from functions import wmtc_profile, RK, model
    from data import v  # Este tramo de código lo cambio por la función de camilo
    #start_time = time.time()
    hev = HEV()

    # Runge-Kutta solver
    # Parameters
    dt = 0.01
    t0 = 0
    tf = len(v)
    trk = np.arange(t0, tf, dt)

    # Control commands
    alpha_t = 0.0           # Throttle control [%, 0-1]
    gamma = 1               # Shift gear [-] 1 to 5 gear ratio
    delta_t = 0.0           # Duty cycle [%, 0-1]
    theta = 0            # Road inclination [deg] 0-90 -- 0 --90
    beta_t = 1              # Clutch: 0 - Slipping, 1 - Locked
    brake = 0               # Brake force in perturbation form

    # Control vector
    u = np.array([alpha_t, gamma, delta_t, theta*math.pi/180, beta_t, brake])

    # Initial conditions
    vhev_0 = 0                      # Initial velocity [Km/h]
    phev_0 = 0                      # Initial position [m]
    iind_0 = 0                      # Initial current armature [A]
    um_0 = delta_t * hev.Buck.ub    # Initial buck current [A]
    im_0 = um_0 / hev.Buck.rp       # Initial buck voltage [V]
    soc_0 = init_soc
    wice_0 = 1000                   # Initial Wice [RPM]
    i_r1_0 = im_0*delta_t

    # Initial cond and control
    x0 = np.array([vhev_0/3.6, phev_0, iind_0, im_0, um_0, soc_0, wice_0/9.5493, i_r1_0]).T    # Initial conditions vector
    delta = np.array([alpha_t, gamma, delta_t, theta*math.pi/180, beta_t, brake]).T

    xrk = np.zeros((len(np.arange(0, len(trk))), 8))   # State vector time
    xrk[0, :] = x0                                     # State vector time
    urk = np.zeros((len(np.arange(0, len(trk))), 6))    # Control vector time
    urk[0, :] = delta                                  # Control vector time

    # Load reference profile
    v_profile = wmtc_profile(dt, t0, tf, v)/3.60

    # Control parameters
    # Throttle
    k_pt = 12
    k_it = 1.5
    k_dt = 0.4
    # duty cycle
    k_pd = 12
    k_id = 1.3
    k_dd = 0.5
    # Brake control
    k_pb = 2
    k_ib = 1.5
    k_db = 0.4

    lasterror = 0
    error = 0
    cumerror = 0

    # Energy contribution
    # electric --> 0.0
    # combustion --> 1.0
    u_contr = hybrid_cont

    # Simulation routine
    for i in np.arange(1, len(trk)):

        vreq = v_profile[i]     # ECE-r15 profile

        # Velocity feedback
        lasterror = error
        error = vreq - x0[0]
        # integral error
        cumerror = cumerror + error * dt
        # Rate error
        rateerror = (error - lasterror) / dt

        # Proportional
        p_alpha = k_pt * error
        p_delta = k_pd * error
        p_brake = -k_pb * error

        # Derivative
        d_alpha = k_dt * rateerror
        d_delta = k_dd * rateerror
        d_brake = -k_db * rateerror

        # Integrative
        i_alpha = k_it * cumerror
        i_delta = k_id * cumerror
        i_brake = -k_ib * cumerror

        # ================= Hybrid Control ==============================
        if error > 0:
            alpha_t = u_contr * (p_alpha + i_alpha + d_alpha)
            delta_t = (1 - u_contr) * (p_delta + i_delta + d_delta)
            beta_t = 1
            brake = 0
        else:
            alpha_t = 0
            delta_t = 0
            beta_t = 1
            brake = p_brake + i_brake

        # Gear box control
        if x0[0] < 10/3.6:
            gamma = 1
        elif (x0[0] >= 10/3.6) and (x0[0] < 15/3.6):
            gamma = 2
        elif (x0[0] >= 15/3.6) and (x0[0] < 25/3.6):
            gamma = 3
        elif (x0[0] >= 25/3.6) and (x0[0] < 41/3.6):
            gamma = 4
        elif x0[0] >= 41/3.6:
            gamma = 5

        # Sat controls
        if delta_t > 1:     # Upper limit
            delta_t = 1
        if delta_t < -1:    # Lower limit
            delta_t = -0.0
        if alpha_t > 1:     # Upper limit
            alpha_t = 1
        if alpha_t < 0:     # Lower limit
            alpha_t = 0
        if brake > 1:     # Upper limit
            brake = 1
        if brake < 0:     # Lower limit
            brake = 0

        delta = np.array([alpha_t, gamma, delta_t, theta * math.pi / 180, beta_t, brake]).T

        # Runge-kutta solver method
        xi = RK(trk[i], dt, x0, delta)
        xrk[i, :] = xi
        x0 = xi
        urk[i, :] = delta

    # plot
    fig, axs = plt.subplots(2)
    axs[0].plot(trk, xrk[:, 0]*3.6)
    axs[0].set_title('Velocity [km/h]')
    axs[0].grid(color='b', ls='-.', lw=0.25)
    axs[1].plot(trk, xrk[:, 5], 'tab:blue')
    axs[1].set_title('SOC [%]')
    axs[1].grid(True)
    plt.show()

    # output
    soc_output = xrk[:, 5]
    #print("--- %s seconds ---" % (time.time() - start_time))
    return soc_output
