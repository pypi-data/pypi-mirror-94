"""Not a public module in version 1.0.0-alpha4."""
#   ***********************************************************************
#
#   FILE         clustering.py
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


def ExternalFlowClustering(Xi, Eta, Beta, Height):
    """Return the clustered grid near the X-lo or Y-lo wall boundaries.

    This function is not complete or tested for accuracy.
    """
    shapeX = Xi.shape()
    iMax, jMax = shapeX

    # If clustering is required near Y = 0.0 surface in positive Y
    # direction.
    Beta1 = (Beta+1.0) / (Beta-1.0)

    X = Xi.copy()
    Y = Eta.copy()
    Y[:, :] = (
        Height * ((Beta+1.0) - (Beta-1.0)) * Beta1**(1.0-Eta[:, :])
        / (Beta1**(1.0-Eta[:, :]) + 1.0)
        )

    return X, Y
