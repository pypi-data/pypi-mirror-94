import preprocess.readfiles as rf
import preprocess.coefficients as coeff
import fluid.parabolicsolvers as pb
import postprocess.residual as res
import postprocess.writetofiles as write
import preprocess.boundary as bound
from importlib import reload
import benchmark.heatconduction as bm
#reload(pb)
#**************************************************************************
configfile = "./input/config.ini"
# Create class instance
cfg = rf.RunConfig(configfile)
U = cfg.U
Error = 1.0
Uold = U.copy
diffX, diffY = coeff.DiffusionNumbers(cfg.Dimension, cfg.diff, cfg.dT,\
                                      cfg.dX, cfg.dY)
# start iterations
n = 0
while n < cfg.nMax and Error > cfg.ConvCrit:
    Error = 0.0
    n = n + 1    
    '''if n == 1:
        U = pb.FTCS(Uold, diffX, diffY)
    Uold2 = Uold.copy()'''
    Uold = U.copy()
    U = pb.ADI(cfg, Uold, diffX, diffY)
    Error = res.AbsoluteError(U, Uold)
    #U = bound.BC2D(U, BC)
    res.MonitorConvergence(n, cfg.nDisplay, Error)
    # Write output to file
    write.WriteSolutionToFile(cfg, n, U)
    # Write convergence history log to a file
    write.WriteConvHistToFile(cfg, n, Error)
write.WriteSolutionIn1DFormat(cfg, U)
# Calculate Analytical solution
#Tana = bm.HeatConduction(100.0, 0.0, 0.0, 0.0, 20)
#write.WriteSolutionIn1DFormat(Tana, "./output/analytic1Dx.dat", cfg.nodes,\
                              #cfg.PrintNodesDir)

print("Exiting.")
