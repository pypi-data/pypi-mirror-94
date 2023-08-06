
def test_analyt():
    '''Test viscous Burgers analytical solution routine.'''
    import nanpack.grid as grid
    import nanpack.benchmark as bm
    import matplotlib.pyplot as plt
    import numpy as np
    x, _ = grid.RectangularGrid(0.2, 91)
    Uanaly = bm.ViscousBurgersSolution(1, x, 0.1)
    ax = plt.subplot()
    plt.plot(x,Uanaly)
    plt.xticks(np.arange(-9.0, 10.0, 3.0))
    plt.yticks(np.arange(round(min(Uanaly)), round(max(Uanaly)+1), 1.0))
    plt.show()

if __name__ == '__main__':
    test_analyt()
    


