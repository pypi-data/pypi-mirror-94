from pyarma import *

def main():
  
  # directly specify the matrix size (elements are set to zero)
  A = mat(2,3)  
  
  # explicit element initialisation during initialisation via one of:
  # fill.zeros, fill.ones, fill.eye, fill.randu,  fill.randn
  A = mat(2,3,fill.zeros)
  
  # .n_rows and .n_cols are read only
  print("A.n_rows: " + str(A.n_rows)) 
  print("A.n_cols: " + str(A.n_cols))
  
  # directly access an element (indexing starts at 0)
  A[1,2] = 456.0 
  A.print("A:")
  
  # change the size (data is not preserved)
  A.set_size(4,5) 
  
  # set all elements to a particular value
  A.fill(5.0) 
  A.print("A:")
  
  # initialisation via lists
  A = mat([ [ 0.165300, 0.454037, 0.995795, 0.124098, 0.047084 ],
            [ 0.688782, 0.036549, 0.552848, 0.937664, 0.866401 ],
            [ 0.348740, 0.479388, 0.506228, 0.145673, 0.491547 ],
            [ 0.148678, 0.682258, 0.571154, 0.874724, 0.444632 ],
            [ 0.245726, 0.595218, 0.409327, 0.367827, 0.385736 ] ])
  
  A.print("A:")
  
  # determinant
  print("det(A): " + str(det(A)))
  
  # inverse
  inv(A).print("inv(A): ")
  
  # save matrix as a text file
  A.save("A.txt", raw_ascii)
  
  # load from file
  B = mat()
  B.load("A.txt")
  
  # transpose
  B.t().print("B.t(): ")
  
  # matrix multiplication
  C = A * B.t()
  C.print("C:")
  
  # element-wise multiplication
  C = A @ B
  C.print("C:")
  
  # submatrices
  C[ 0:2, 3:4 ].print("C[ 0:2, 3:4 ]:")
  
  C[ 0,3, size(3,2) ].print("C[ 0,3, size(3,2) ]:")
  
  C[0, :].print("C[0, :]: ")
  
  C[:, 0].print("C[:, 0]: ")
  
  # maximum from each column (traverse along rows)
  max(C).print("max(C): ")
  
  # maximum from each row (traverse along columns)
  max(C,1).print("max(C,1): ")
  
  # maximum value in C
  print("max(max(C)) = " + str(as_scalar(max(max(C)))))
  
  # sum of each column (traverse along rows)
  sum(C).print("sum(C): ")
  
  # sum of each row (traverse along columns)
  sum(C,1).print("sum(C,1): ")
  
  # sum of all elements
  print("accu(C): " + str(accu(C)))
  
  # trace = sum along main diagonal
  print("trace(C): " + str(trace(C)))
  
  # convert matrix to vector; data in matrices is stored column-by-column
  v = vectorise(A)
  v.print("v:")
  
  # example of a compound operation
  B += 2.0 * A.t()
  B.print("B:")
  
  # imat specifies an integer matrix
  AA = imat([ [ 1, 2, 3 ],
              [ 4, 5, 6 ],
              [ 7, 8, 9 ] ])
  
  BB = imat([ [ 3, 2, 1 ],
              [ 6, 5, 4 ],
              [ 9, 8, 7 ] ])
  
  # comparison of matrices (element-wise); output of a relational operator is a umat
  ZZ = (AA >= BB)
  ZZ.print("ZZ:")
  
  # cubes ("3D matrices")
  Q = cube( B.n_rows, B.n_cols, 2 )
  
  Q[single_slice, 0] = B
  Q[single_slice, 1] = 2.0 * B
  
  Q.print("Q:")



if __name__ == "__main__":
    main()
