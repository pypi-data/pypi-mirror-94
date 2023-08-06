import preprocess.readfiles as rf
import preprocess.coefficients as coeff
import fluid.hyperbolicsolvers as hb
import postprocess.residual as res
import postprocess.writetofiles as write
import math
import matplotlib.pyplot as plt
fig, ax = plt.subplots(dpi=150)
cfg = rf.RunConfig("./input/config.ini")
U = cfg.U
# initial
i1 = int(50/cfg.dX+1)
i2 = int(110/cfg.dX+1)
U[0:i1] = 0.0
U[i1:i2] = [100.0*math.sin(math.pi*(cfg.dX*i - 50)/60) for i in range(i1,i2)]
U[i2:] = [0.0 for i in range (i2,cfg.iMax)]
# plot initial data
#ax.minorticks_on()
#ax.grid(which='major', axis='both', color='blue', linestyle='--',\
#        linewidth=0.5)
#ax.grid(which='minor', axis='both', color='lightgrey', linestyle=':',\
#        linewidth=0.5)
#X = [cfg.dX*i for i in range(cfg.iMax)]
#ax.plot(X, U, color='black')
#plt.xlabel('X (m)')
#plt.ylabel('Velocity (m/s)')
#plt.title('Initial distribution of wave\nat t=0.0 s', fontsize=10)
#plt.show()

# bc
U[0] = 0.0
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
    U = hb.EulersBTCS(cfg, Uold, cfg.CFL)
    Error = res.AbsoluteError(U, Uold)
    # update BC
    U[0] = 0.0
    U[-1] = 0.0
    res.MonitorConvergence(n, cfg.nDisplay, Error)    
    # Write output to file
    write.WriteSolutionToFile(cfg, n, U)
    # Write convergence history log to a file
    write.WriteConvHistToFile(cfg, n, Error)
print("Exiting.")
