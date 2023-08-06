import preprocess.readfiles as rf
import fluid.ellipticsolvers as ep
import postprocess.residual as res
import postprocess.writetofiles as write
from importlib import reload
import benchmark.heatconduction as bm
#reload(pb)
#**************************************************************************
configfile = "./input/config.ini"
# Create class instance
cfg = rf.RunConfig(configfile)
Error = 1.0
U = cfg.U
# start iterations
n = 0
while n < cfg.nMax and Error > cfg.ConvCrit:
    Error = 0.0
    n = n + 1
    Uold = U.copy()
    '''if n == 1:
        U = pb.FTCS(Uold, diffX, diffY)
    Uold2 = Uold.copy()'''
    U = ep.ADISOR(cfg, Uold)
    Error = res.AbsoluteError(U, Uold)
    #U = bound.BC2D(U, BC)
    res.MonitorConvergence(n, cfg.nDisplay, Error)
    # Write output to file
    write.WriteSolutionToFile(cfg, n, U)
    # Write convergence history log to a file
    write.WriteConvHistToFile(cfg, n, Error)

# Write output to file
print(n)
write.WriteSolutionToFile(cfg, n, U)
# Write convergence history log to a file
write.WriteConvHistToFile(cfg, n, Error)
write.WriteSolutionIn1DFormat(cfg, U)
# Calculate Analytical solution
Tana = bm.HeatConduction(cfg, 100.0, 0.0, 0.0, 0.0, 20)
write.WriteSolutionIn1DFormat(cfg, Tana, "./output/analytic1Dx.dat")

print("Exiting.")
