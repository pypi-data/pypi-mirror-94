
from numpy import where, dstack, diff, meshgrid
import numpy as np

def orientation(p, q, r):
  """Orientation of triplet (p,q,r)

  Returns:
    -1 if counterclockwise
    0 if colinear
    1 if clockwise"""
  
  da = q - p
  db = r - q
  C = da[:,::-1]*db
  return np.sign(C[:,0] - C[:,1])

def intersects(A1, A2, B1, B2):

  o1 = orientation(A1, A2, B1)
  o2 = orientation(A1, A2, B1)
  o3 = orientation(A1, A2, B1)
  o4 = orientation(A1, A2, B1)
  
  dA = A2 - A1
  da1 = B1 - A2
  da2 = B2 - A2
  
  dB = B2 - B1
  db1 = A1 - B2
  db2 = A2 - B2


def find_intersections(A, B):

    # min, max and all for arrays
    amin = lambda x1, x2: where(x1<x2, x1, x2)
    amax = lambda x1, x2: where(x1>x2, x1, x2)
    aall = lambda abools: dstack(abools).all(axis=2)
    slope = lambda line: (lambda d: d[:,1]/d[:,0])(diff(line, axis=0))

    x11, x21 = meshgrid(A[:-1, 0], B[:-1, 0])
    x12, x22 = meshgrid(A[1:, 0], B[1:, 0])
    y11, y21 = meshgrid(A[:-1, 1], B[:-1, 1])
    y12, y22 = meshgrid(A[1:, 1], B[1:, 1])

    m1, m2 = meshgrid(slope(A), slope(B))
    m1inv, m2inv = 1/m1, 1/m2

    yi = (m1*(x21-x11-m2inv*y21) + y11)/(1 - m1*m2inv)
    xi = (yi - y21)*m2inv + x21

    xconds = (amin(x11, x12) < xi, xi <= amax(x11, x12), 
              amin(x21, x22) < xi, xi <= amax(x21, x22) )
    yconds = (amin(y11, y12) < yi, yi <= amax(y11, y12),
              amin(y21, y22) < yi, yi <= amax(y21, y22) )

    return xi[aall(xconds)], yi[aall(yconds)]

T = np.array([[0, -1], [1, 0]])
def line_intersect(a1, a2, b1, b2):
    da = np.atleast_2d(a2 - a1)
    db = np.atleast_2d(b2 - b1)
    dp = np.atleast_2d(a1 - b1)
    dap = np.dot(da, T)
    denom = np.sum(dap * db, axis=1)
    num = np.sum(dap * dp, axis=1)
    return np.atleast_2d(num / denom).T * db + b1
