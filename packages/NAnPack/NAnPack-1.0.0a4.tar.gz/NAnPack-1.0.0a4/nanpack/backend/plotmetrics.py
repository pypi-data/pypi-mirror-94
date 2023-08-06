"""Not a public module in 1.0.0a4."""
#   ***********************************************************************
#
#   FILE         plotmetrics.py
#
#   AUTHOR       Dr. Vishal Sharma
#
#   VERSION      1.0.0-alpha4
#
#   WEBSITE      https://github.com/vxsharma-14/project-NAnPack
#
#   NAnPack Learner's Edition is distributed under the MIT License.
#
#   Copyright (c) 2020 Vishal Sharma
#
#   Permission is hereby granted, free of charge, to any person
#   obtaining a copy of this software and associated documentation
#   files (the "Software"), to deal in the Software without restriction,
#   including without limitation the rights to use, copy, modify, merge,
#   publish, distribute, sublicense, and/or sell copies of the Software,
#   and to permit persons to whom the Software is furnished to do so,
#   subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
#   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
#   ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#
#   You should have received a copy of the MIT License along with
#   NAnPack Learner's Edition.
#
#   ***********************************************************************


def PlotMetrics2D(X, Y, XiX, XiY, EtaX, EtaY):
    """Show the plot of the metrics of the transformation."""
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import axes3d

    shape = XiX.shape
    im, jm = shape

    # Assign fonts in the figure
    plt.rc('font', family='serif', size=9)

    fig = plt.figure(dpi=150)

    # Reshape data based on IM and JM
    x = np.reshape(X, (im, jm))
    y = np.reshape(Y, (im, jm))
    z1 = np.reshape(XiX, (im, jm))
    z2 = np.reshape(XiY, (im, jm))
    z3 = np.reshape(EtaX, (im, jm))
    z4 = np.reshape(EtaY, (im, jm))
    ttl = ['XiX',
           'XiY',
           'EtaX',
           'EtaY'
           ]

    for i in range(1, 5):
        ax = fig.add_subplot(2, 2, i, projection='3d')

        # Generate plot for the data
        if i == 1:
            ax.plot_wireframe(x, y, z1)
        elif i == 2:
            ax.plot_wireframe(x, y, z2)
        elif i == 3:
            ax.plot_wireframe(x, y, z3)
        else:
            ax.plot_wireframe(x, y, z4)
        # define plot properties
        plt.xlabel('\n\nX (m)', size=8)
        plt.ylabel('\n\nY (m)', size=8)
        plt.title(f'{ttl[i-1]} Metrics', size=10)
        ax.set_zlim(-20.0, 20.0)
        plt.xticks(size=8, rotation=30)
        plt.yticks(size=8, rotation=-30)

        plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.05, hspace=0.2,
                        wspace=0.01)
    plt.show()
