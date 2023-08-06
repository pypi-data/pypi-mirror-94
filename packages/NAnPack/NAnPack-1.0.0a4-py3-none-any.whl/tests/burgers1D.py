import preprocess.readfiles as rf
import preprocess.coefficients as coeff
import fluid.hyperbolicsolvers as hb
import fluid.secondaryfunctions as func
import postprocess.residual as res
import postprocess.writetofiles as write
import math
import matplotlib.pyplot as plt
import fluid.tvdfunctions as tvd
fig, ax = plt.subplots(dpi=150)
cfg = rf.RunConfig("./input/config.ini")
U = cfg.U
# initial
i1 = int(2.0/cfg.dX+1)
U[0:i1] = 1.0
U[i1:] = 0.0
choice = 'N'
#choice = input("Do you want to plot the initial data? (Y/N)\n")
if choice == 'Y':
    # plot initial data
    ax.minorticks_on()
    ax.grid(which='major', axis='both', color='blue', linestyle='--',\
            linewidth=0.5)
    ax.grid(which='minor', axis='both', color='lightgrey', linestyle=':',\
            linewidth=0.5)
    X = [cfg.dX*i for i in range(cfg.iMax)]
    ax.plot(X, U, color='black')
    plt.xlabel('X (m)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Initial distribution\nat t=0.0 s', fontsize=10)
    plt.show()

# bc
U[0] = 1.0
U[-1] = 0.0
Error = 1.0
#Uold = U.copy()
# start iterations
n = 0
while n<cfg.nMax:
    Error = 0.0
    n+=1
    '''
    if n == 1:
        U[1:-1] = U[1:-1]\
                  + diffX*(U[2:] - 2.0*U[1:-1] + U[0:-2])
    Uold2 = Uold.copy()'''
    Uold = U.copy()
    U = hb.ModifiedRungeKutta(cfg, Uold, cfg.CFL)
    E = Uold*Uold/2
    #U = hb.SecondOrderTVD(cfg, Uold, cfg.CFL, "Davis-Yee-Symmetric", "G3")
    for i in range(2,cfg.iMax-2):
        phiP, phiM = tvd.DavisYeeSymmetric(i, Uold, E, 0.01, cfg.CFL, 'G1')
        U[i] = U[i] -0.5*cfg.CFL*(phiP - phiM)
    Error = res.AbsoluteError(U, Uold)
    # update BC
    U[0] = 1.0
    U[-1] = 0.0
    # add damping
    #D = func.FourthOrderDamping(Uold, 0.1)
    #U[2:-2] = U[2:-2] + D[2:-2]
    # monitor convergence
    res.MonitorConvergence(n, cfg.nDisplay, Error)    
    # Write output to file
    write.WriteSolutionToFile(cfg, n, U)
    # Write convergence history log to a file
    write.WriteConvHistToFile(cfg, n, Error)
print("Exiting.")
