import nanpack

cfg = rf.RunConfig("./input/config.ini")
U = cfg.U
# bc
U[0] = 40.0
U[-1] = 0.0
Error = 1.0
Uold = U.copy()
# start iterations
n = 0
diffX,_ = coeff.DiffusionNumbers(cfg.Dimension, cfg.diff, cfg.dT,\
                                cfg.dX)
while n<cfg.nMax:
    Error = 0.0
    n+=1
    if n == 1:
        U[1:-1] = U[1:-1]\
                  + diffX*(U[2:] - 2.0*U[1:-1] + U[0:-2])
    Uold2 = Uold.copy()
    Uold = U.copy()
    U = pb.DuFortFrankel(Uold, Uold2, diffX)
    Error = res.AbsoluteError(U, Uold)
    U[0] = 40.0
    U[-1] = 0.0
    res.MonitorConvergence(n, cfg.nDisplay, Error)    
    # Write output to file
    write.WriteSolutionToFile(cfg, n, U)
    # Write convergence history log to a file
    write.WriteConvHistToFile(cfg, n, Error)
print("Exiting.")
