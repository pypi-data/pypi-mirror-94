from pyarma import *

# cx_fmat class
A = cx_fmat(5, 5, fill.randu)
x = A[1,2]

M = umat(5, 5, fill.ones) # initialise 5x5 matrix with ones
N = cx_fmat(M)                # convert to double-precision floating point

B = A + A
C = A * B
D = A @ B

# X = cx_mat(A,B)

B.zeros()
B.set_size(10,10)
B.ones(5,6)

B.print("B:")

# Operations
A = cx_fmat(5, 10, fill.randu)
B = cx_fmat(5, 10, fill.randu)
C = cx_fmat(10, 5, fill.randu)

P = A + B
Q = A - B
R = -B
# TODO: FIX THIS
# S = A / 123.0
T = A @ B
U = A * C

AA = umat("1 2 3; 4 5 6; 7 8 9;")
BB = umat("3 2 1; 6 5 4; 9 8 7;")

# compare elements
ZZ = (AA >= BB)

# broadcasting
X = cx_fmat(6, 5, fill.ones)
v = cx_fmat(6, 1, fill.randu)

# in-place addition of v to each column vector of X
X += v

# generate Y by adding v to each column vector of X
Y = X + v 

# attributes
X = cx_fmat(4,5)
print("X has " + str(X.n_cols) + " columns")

# indexing
A = cx_fmat(10, 10, fill.randu)
A[9,9] = 123.0
x = A[9,9]
y = A[99]

# element initialisation
v = cx_fmat([ 1, 2, 3 ])
A = cx_fmat([ [1, 3, 5],
          [2, 4, 6] ])

# member zeros
A = cx_fmat(5,10)
A.zeros()   
# or:  A = cx_fmat(5,10,fill.zeros)

B = cx_fmat()
B.zeros(10,20)

C = cx_fmat()
C.zeros( size(B) )

# member ones
A = cx_fmat(5,10)
A.ones()
# or:  A = cx_fmat(5,10,fill.ones)

B = cx_fmat()
B.ones(10,20)

C = cx_fmat()
C.ones( size(B) )

# member eye
A = cx_fmat(5,5)
A.eye()
# or:  A = cx_fmat(5,5,fill.eye)

B = cx_fmat()
B.eye(5,5)

C = cx_fmat()
C.eye( size(B) )

# randu/randn
A = cx_fmat(5,10)
A.randu()
# or:  A = cx_fmat(5,10,fill.randu)

B = cx_fmat()
B.randu(10,20)

C = cx_fmat()
C.randu( size(B) )

pyarma_rng.set_seed_random()  # set the seed to a random value

# fill
A = cx_fmat(5, 6)
# A.fill(123.0)
# A.fill(123) is also accepted and has the same result
A = cx_fmat(5, 6, fill.zeros)

#imbue
from random import uniform
  
A = cx_fmat(4, 5)
  
A.imbue( lambda: uniform(0, 1) )

# clean
A = cx_fmat()

A.randu(1000, 1000)

A[12,34] =  datum.eps
A[56,78] = -datum.eps

A.clean(datum.eps)

# replace
A = cx_fmat(5, 6, fill.randu)

A[diag].fill(datum.nan)

# TODO: FIX THIS
# A.replace(datum.nan, 0) # replace each NaN with 0

#transform
A = cx_fmat(4, 5, fill.ones)

# add 123 to every element
A.transform( lambda val: val + 123.0 )

# for_each
# print each element in a dense matrix

A = cx_fmat(4, 5, fill.ones)

A.for_each( lambda val: print(val) )

# set_size
A = cx_fmat()
A.set_size(5,10)       # or:  A = cx_fmat(5,10)

B = cx_fmat()
B.set_size( size(A) )  # or:  B = cx_fmat( size(A) )

# reshape
A = cx_fmat(4, 5, fill.randu)

A.reshape(5,4)

# resize
A = cx_fmat(4, 5, fill.randu)

A.resize(7,6)

# copy_size

A = cx_fmat(5, 6, fill.randu)
B = cx_fmat()
B.copy_size(A)

# reset
A = cx_fmat(5, 5, fill.randu)
A.reset()

print(str(B.n_rows))
print(str(B.n_cols))

# reset
A = cx_fmat(5, 5, fill.randu)
A.reset()

# submatrix
A = cx_fmat(5, 10, fill.zeros)

A[ 0:2, 1:3 ]             = cx_fmat(3,3, fill.randu)
# A[ span(0,2), span(1,3) ] = cx_fmat(3,3, fill.randu)
# A[ 0,1, size(3,3) ]       = cx_fmat(3,3, fill.randu)

B = A[ 0:2, 1:3 ].eval()
# C = A[ span(0,2), span(1,3) ].eval()
# D = A[ 0,1, size(3,3) ].eval()

A[:,1]          = cx_fmat(5,1,fill.randu)
# A[span_all, 1]  = cx_fmat(5,1,fill.randu)

X = cx_fmat(5, 5, fill.randu)

# TODO: FIX THIS
# # get all elements of X that are greater than 0.5
# q = X[ find(X > 0.5) ]

# # add 123 to all elements of X greater than 0.5
# X[ find(X > 0.5) ] += 123.0

# set four specific elements of X to 1
indices = umat([ 2, 3, 6, 8 ])

X[indices] = cx_fmat(4,1,fill.ones)

# diagonal
X = cx_fmat(5, 5, fill.randu)

a = X[diag]
b = X[diag, 1]
c = X[diag, -2]

X[diag] = cx_fmat(5,1,fill.randu)
# TODO: FIX THIS
# X[diag] += 6
X[diag].ones()

# set_real, set_imag
A = fmat(4, 5, fill.randu)
B = fmat(4, 5, fill.randu)

C = cx_mat(4, 5, fill.zeros)

C.set_real(A)
C.set_imag(B)

# fast cx_mat
A = cx_fmat(4, 5, fill.randu)
B = cx_fmat(4, 5, fill.randu)

# C = cx_mat(A,B)

# ins_row/cols
A = cx_fmat(5, 10, fill.randu)
B = cx_fmat(5,  2, fill.ones )

# at column 2, insert a copy of B;
# A will now have 12 columns
A.insert_cols(2, B)

# at column 1, insert 5 zeroed columns;
# B will now have 7 columns
B.insert_cols(1, 5)

# shed_row/cols
A = cx_fmat(5, 10, fill.randu)
B = cx_fmat(5, 10, fill.randu)

A.shed_row(2)
A.shed_cols(2,4)

indices = umat([4, 6, 8])
B.shed_cols(indices)

#swap_rows
X = cx_fmat(5, 5, fill.randu)
X.swap_rows(0,4)

# swap
A = cx_fmat(4, 5, fill.zeros)
B = cx_fmat(6, 7, fill.ones )

A.swap(B)

# iterators
X = cx_fmat(5, 6, fill.randu)

for i in X:                # this prints all elements
  print(i)

it = iter(X)               # this also prints all elements
for i in it:
  print(i)

col_it = col_iter(X, 1, 3) # start of column 1 and end of column 3

for i in col_it:
  print(i)

# iterators for submats
X = cx_fmat(100, 200, fill.randu)

for val in X[40:60, 50:100]:
  print(val)

# as_col
X = cx_fmat(4, 5, fill.randu)
v = X.as_col()

#trans
A = cx_fmat(4, 5, fill.randu)
B = A.t()

#inv
A = cx_fmat(4, 4, fill.randu)

X = A.i()

Y = (A+A).i()

#max
A = cx_fmat(5, 5, fill.randu)

max_val = A.max()

#ind_max
A = cx_fmat(5, 5, fill.randu)

i = A.index_max()

max_val = A[i]

#eval
A = umat(4,4,fill.ones)

# Any change to B does not affect A
B = A[0:1, 2:3].eval()

B[0,0] = 5

# Therefore, B and A[0:1, 2:3] should not be equal
(B == A[0:1, 2:3]).print()

#in_range
A = cx_fmat(4, 5, fill.randu)

print(A.in_range(0,0))  # true
print(A.in_range(3,4))  # true
print(A.in_range(4,5))  # false

#is_empty
A = cx_fmat(5, 5, fill.randu)
print(A.is_empty())

A.reset()
print(A.is_empty())


#is_vec
A = cx_fmat(1, 5, fill.randu)
B = cx_fmat(5, 1, fill.randu)
C = cx_fmat(5, 5, fill.randu)

print(A.is_vec())
print(B.is_vec())
print(C.is_vec())

#is_sorted
a = cx_fmat(10, 1, fill.randu)
b = sort(a)

check1 = a.is_sorted()
check2 = b.is_sorted()

A = cx_fmat(10, 10, fill.randu)

# check whether each column is sorted in descending manner
print(A.is_sorted("descend"))

# check whether each row is sorted in ascending manner
print(A.is_sorted("ascend", 1))

# is_trimatu/l
A = cx_fmat(5, 5, fill.randu)
B = trimatl(A)

print(A.is_trimatu())
print(B.is_trimatl())

#is_diagmat
A = cx_fmat(5, 5, fill.randu)
B = diagmat(A)

print(A.is_diagmat())
print(B.is_diagmat())

#is_square
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(6, 7, fill.randu)

print(A.is_square())
print(B.is_square())

#is_symm
A = cx_fmat(5, 5, fill.randu)
B = A.t() * A

print(A.is_symmetric())
print(B.is_symmetric())

#is_hermitian
cx_A = cx_mat(5, 5, fill.randu)
cx_B = A.t() * A

print(A.is_hermitian())
print(B.is_hermitian())

#is_sympd
A = cx_fmat(5, 5, fill.randu)

B = A.t() * A

print(A.is_sympd())
print(B.is_sympd())

#is_zero
A = cx_fmat(5, 5, fill.zeros)

A[0,0] = datum.eps

print(A.is_zero())
print(A.is_zero(datum.eps))

#is_finite
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(5, 5, fill.randu)

B = cx_fmat(1,1)
B[0,0] = datum.inf

print(A.is_finite())
print(B.is_finite())

#has_inf
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(5, 5, fill.randu)

B = cx_fmat(1,1)
B[0,0] = datum.inf

print(A.has_inf())
print(B.has_inf())

#has_nan
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(5, 5, fill.randu)

B = cx_fmat(1,1)
B[0,0] = datum.nan

print(A.has_nan())
print(B.has_nan())

#print
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(6, 6, fill.randu)

A.print()

# print a transposed version of A
A.t().print()

# "B:" is the optional header line
B.print("B:")

#save/load
A = cx_fmat(5, 6, fill.randu)

# default save format is arma_binary
A.save("A.bin")

# save in raw_ascii format
A.save("A.txt", raw_ascii)

# save in CSV format without a header
A.save("A.csv", csv_ascii)

# save in HDF5 format
# A.save("A.h5", hdf5_binary)

# automatically detect format type while loading
B = cx_fmat()
B.load("A.bin")

# force loading in arma_ascii format
C = cx_fmat()
C.load("A.txt", arma_ascii)

# example of testing for success
D = cx_fmat()
ok = D.load("A.bin")

if not ok:
  print("problem with loading")

#linspace
a = linspace(0, 5, 6)

#logspace
a = logspace(0, 5, 6)

#regspace
a = regspace(0,  9)       # 0,  1, ...,   9

b = regspace(2,  2,  10)  # 2,  4, ...,  10

#randperm
X = randperm(10)
Y = randperm(10,2)

#toeplitz
A = cx_fmat(5, 1, fill.randu)
X = toeplitz(A)
Y = circ_toeplitz(A)

# abs
A = cx_fmat(5, 5, fill.randu)
B = abs(A) 

X = cx_mat(5, 5, fill.randu)
Y = abs(X)

# accu
A = cx_fmat(5, 6, fill.randu)
B = cx_fmat(5, 6, fill.randu)

x = accu(A)

y = accu(A @ B)

# accu(A @ B) is a "multiply-and-accumulate" operation
# as operator @ performs element-wise multiplication

# TODO: FIX THIS
#all
V = cx_fmat(10,1, fill.randu)
X = cx_fmat(5, 5, fill.randu)

# status1 will be set to true if vector V has all non-zero elements
status1 = all(V)

# status2 will be set to true if vector V has all elements greater than 0.5
# status2 = all(V > 0.5)

# status3 will be set to true if matrix X has all elements greater than 0.6;
# note the use of vectorise()
# status3 = all(vectorise(X) > 0.6)
# 
# generate a row vector indicating which columns of X have all elements greater than 0.7
# uA = all(X > 0.7)

#any
V = cx_fmat(10,1, fill.randu)
X = cx_fmat(5, 5, fill.randu)

# status1 will be set to true if vector V has any non-zero elements
status1 = any(V)

# status2 will be set to true if vector V has any elements greater than 0.5
# status2 = any(V > 0.5)

# status3 will be set to true if matrix X has any elements greater than 0.6;
# note the use of vectorise()
# status3 = any(vectorise(X) > 0.6)

# generate a row vector indicating which columns of X have elements greater than 0.7
# uA = any(X > 0.7)

# TODO: FIX THIS
#approx_equal
A = cx_fmat(5, 5, fill.randu)
# B = A + 0.001

same1 = approx_equal(A, B, "absdiff", 0.002)

# C = 1000 * cx_fmat(5,5, fill.randu)
# D = C + 1

same2 = approx_equal(C, D, "reldiff", 0.1)

same3 = approx_equal(C, D, "both", 2, 0.1)

#arg
A = cx_mat(5, 5, fill.randu)
B = arg(A)

#as_scalar
r = cx_fmat(1, 5, fill.randu)
q = cx_fmat(5, 1, fill.randu)

X = cx_fmat(5, 5, fill.randu)

a = as_scalar(r*q)
b = as_scalar(r*X*q)
c = as_scalar(r*diagmat(X)*q)
d = as_scalar(r*inv(diagmat(X))*q)

# #clamp
# A = cx_fmat(5, 5, fill.randu )

# B = clamp(A, 0.2,     0.8) 

# C = clamp(A, A.min(), 0.8) 

# D = clamp(A, 0.2, A.max()) 

#cond
A = cx_fmat(5, 5, fill.randu)
c = cond(A)

#conj
X = cx_mat(5, 5, fill.randu)
Y = conj(X)

#cross
a = cx_fmat(3, 1, fill.randu)
b = cx_fmat(3, 1, fill.randu)

c = cross(a,b)

#cumsum
A = cx_fmat(5, 5, fill.randu)
B = cumsum(A)
C = cumsum(A, 1)

x = cx_fmat(10, 1, fill.randu)
y = cumsum(x)

#cumprod
A = cx_fmat(5, 5, fill.randu)
B = cumprod(A)
C = cumprod(A, 1)

x = cx_fmat(10, 1, fill.randu)
y = cumprod(x)

#det
A = cx_fmat(5, 5, fill.randu)

x = det(A)

#diagmat
A = cx_fmat(5, 5, fill.randu)
B = diagmat(A)
C = diagmat(A,1)

v = cx_fmat(5, 1, fill.randu)
D = diagmat(v)
E = diagmat(v,1)

#diagvec
A = cx_fmat(5, 5, fill.randu)

d = diagvec(A)

#diff
a = linspace(1,10,10)

b = diff(a)

#dot
a = cx_fmat(10, 1, fill.randu)
b = cx_fmat(10, 1, fill.randu)

x = dot(a,b)

#eps
A = cx_fmat(4, 5, fill.randu)
B = eps(A)

#expmat
A = cx_fmat(5, 5, fill.randu)

B = expmat(A)

#expmat_sym
A = cx_fmat(5, 5, fill.randu)

B = A*A.t()   # make symmetric matrix

C = expmat_sym(B)

#find
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(5, 5, fill.randu)

# q1 = find(A > B)
# q2 = find(A > 0.5)
# q3 = find(A > 0.5, 3, "last")

# # change elements of A greater than 0.5 to 1
# A[ find(A > 0.5) ].ones()

#find_finite
A = cx_fmat(5, 5, fill.randu)

A[1,1] = datum.inf

# accumulate only finite elements
val = accu( A[ find_finite(A) ] )

#find_nonfinite
A = cx_fmat(5, 5, fill.randu)

A[1,1] = datum.inf
A[2,2] = datum.nan

# change non-finite elements to zero
A[ find_nonfinite(A) ].zeros()

#find_unique
A = cx_fmat([ [ 2, 2, 4 ], 
          [ 4, 6, 6 ] ])

indices = find_unique(A)

#fliplr/ud
A = cx_fmat(5, 5, fill.randu)

B = fliplr(A)
C = flipud(A)

#imag/real
C = cx_mat(5, 5, fill.randu)

A = imag(C)
B = real(C)

#ind2sub
M = cx_fmat(4, 5, fill.randu)

s = ind2sub( size(M), 6 )

print("row: " + str(s[0]))
print("col: " + str(s[1]))


# indices = find(M > 0.5)
t       = ind2sub( size(M), indices )

#index_min/max

v = cx_fmat(10, 1, fill.randu)

i = index_max(v)
max_val_in_v = v[i]


M = cx_fmat(5, 6, fill.randu)

ii = index_max(M)
jj = index_max(M,1)

max_val_in_col_2 = M[ ii[2], 2 ]

max_val_in_row_4 = M[ 4, jj[4] ]

#inplace_trans
X = cx_fmat(4,     5,     fill.randu)
Y = cx_fmat(20, 30, fill.randu)

inplace_trans(X)

inplace_trans(Y)

#intersect
A = regspace(4, 1)  # 4, 3, 2, 1
B = regspace(3, 6)  # 3, 4, 5, 6
A = cx_fmat(A)
B = cx_fmat(B)

C = intersect(A,B)       # 3, 4

CC = cx_fmat()
iA = umat()
iB = umat()

intersect(CC, iA, iB, A, B)

#join
A = cx_fmat(4, 5, fill.randu)
B = cx_fmat(4, 6, fill.randu)
C = cx_fmat(6, 5, fill.randu)

AB = join_rows(A,B)
AC = join_cols(A,C)

#kron
A = cx_fmat(4, 5, fill.randu)
B = cx_fmat(5, 4, fill.randu)

K = kron(A,B)

#log_det
A = cx_fmat(5, 5, fill.randu)
result = log_det(A)

# #logmat
# A = cx_fmat(5, 5, fill.randu)

# B = logmat(A)

#logmat_sympd
A = cx_fmat(5, 5, fill.randu)

B = A*A.t()   # make symmetric matrix

C = logmat_sympd(B)

#max
v = cx_fmat(10, 1, fill.randu)
x = max(v)

M = cx_fmat(10, 10, fill.randu)

a = max(M)
b = max(M,0) 
c = max(M,1)

# element-wise maximum
X = cx_fmat(5, 6, fill.randu)
Y = cx_fmat(5, 6, fill.randu)
Z = max(X,Y)

#nonzeros
B = cx_fmat(100, 100, fill.eye)
b = nonzeros(B)

#norm
q = cx_fmat(5, 1, fill.randu)

x = norm(q, 2)
y = norm(q, "inf")

#normalise
A = cx_fmat(10, 1, fill.randu)
B = normalise(A)
C = normalise(A, 1)

X = cx_fmat(5, 6, fill.randu)
Y = normalise(X)
Z = normalise(X, 2, 1)

#print
A = cx_fmat(123, 456, fill.randu)

print(A)

# possible output:
# 
# <pyarma.pyarma.cx_fmat object at 0x123456>
# [matrix size: 123x456]
#    0.8402   0.7605   0.6218      ...   0.9744
#    0.3944   0.9848   0.0409      ...   0.7799
#    0.7831   0.9350   0.4140      ...   0.8835
#         :        :        :        :        :        
#    0.4954   0.1826   0.9848      ...   0.1918

#prod
v = cx_fmat(10, 1, fill.randu)
x = prod(v)

M = cx_fmat(10, 10, fill.randu)

a = prod(M)
b = prod(M,0)
c = prod(M,1)

#powmat
A = cx_fmat(5, 5, fill.randu)

B = powmat(A, 4)     #     integer exponent

# C = powmat(A, 4.56)  # non-integer exponent

#rank
A = cx_fmat(4, 5, fill.randu)

r = rank(A)

#rcond
A = cx_fmat(5, 5, fill.randu)

r = rcond(A)

#repelem
A = cx_fmat(2, 3, fill.randu)

B = repelem(A, 4, 5)

#repmat
A = cx_fmat(2, 3, fill.randu)

B = repmat(A, 4, 5)

#reshape
A = cx_fmat(10, 5, fill.randu)

B = reshape(A, 5, 10)

#resize
A = cx_fmat(4, 5, fill.randu)

B = resize(A, 7, 6)

#reverse
v = cx_fmat(123, 1, fill.randu)
y = reverse(v)

A = cx_fmat(4, 5, fill.randu)
B = reverse(A)
C = reverse(A,1)

#roots
P = cx_fmat(5, 1, fill.randu)
  
R = roots(P)

#shift
A = cx_fmat(4, 5, fill.randu)
B = shift(A, -1)
C = shift(A, +1)

#size
A = cx_fmat(5,6)

B = cx_fmat(size(A), fill.zeros)

C = cx_fmat()

C.randu(size(A))

D = cx_fmat(10,20, fill.ones)
D[3,4,size(C)] = C    # access submatrix of E

E = cx_fmat( size(A) + size(E) )
G = cx_fmat( size(A) * 2 )
print("size of A: " + str(size(A)))
is_same_size = (size(A) == size(E))

#shuffle
A = cx_fmat(4, 5, fill.randu)
B = shuffle(A)

#sort
A = cx_fmat(10, 10, fill.randu)
B = sort(A)

#sort_index
q = cx_fmat(10, 1, fill.randu)

indices = sort_index(q)

# #sqrtmat
# A = cx_fmat(5, 5, fill.randu)

# B = sqrtmat(A)

#sqrtmat_sympd
A = cx_fmat(5, 5, fill.randu)

B = A*A.t()   # make symmetric matrix

C = sqrtmat_sympd(B)

#sum
v = cx_fmat(10, 1, fill.randu)
x = sum(v)

M = cx_fmat(10, 10, fill.randu)

a = sum(M)
b = sum(M,0)
c = sum(M,1)

y = accu(M)   # find the overall sum regardless of object type

#sub2ind
M = cx_fmat(4,5)

i = sub2ind( size(M), 2, 3 )

#symmat
A = cx_fmat(5, 5, fill.randu)

B = symmatu(A)
C = symmatl(A)

#trace
A = cx_fmat(5, 5, fill.randu)

x = trace(A)

#trans
A = cx_fmat(5, 10, fill.randu)

B = trans(A)
C = A.t()    # equivalent to trans(A), but more compact

#trapz
X = linspace(0, datum.pi, 1000)
Y = sin(X)

Z = trapz(X,Y)

#trimat
A = cx_fmat(5, 5, fill.randu)

U  = trimatu(A)
L  = trimatl(A)

UU = trimatu(A,  1)  # omit the main diagonal
LL = trimatl(A, -1)  # omit the main diagonal

#trimat_ind
A = cx_fmat(5, 5, fill.randu)

upper_indices = trimatu_ind( size(A) )
lower_indices = trimatl_ind( size(A) )

# extract upper/lower triangle into vector
upper_part = A[upper_indices]
lower_part = A[lower_indices]

# obtain indices without the main diagonal
alt_upper_indices = trimatu_ind( size(A),  1)
alt_lower_indices = trimatl_ind( size(A), -1)

#unique
X = cx_fmat([ [ 1, 2 ],
          [ 2, 3 ] ])
Y = unique(X)

#vectorise
X = cx_fmat(4, 5, fill.randu)

v = vectorise(X)

#exp
A = cx_fmat(5, 5, fill.randu)
B = exp(A)

#cos
X = cx_fmat(5, 5, fill.randu)
Y = cos(X)

#chol
X = cx_fmat(5, 5, fill.randu)
Y = X.t()*X

R1 = chol(Y)
R2 = chol(Y, "lower")

#eig_sym
# for matrices with real elements

A = cx_fmat(50, 50, fill.randu)
B = A.t()*A  # generate a symmetric matrix

eigval = fmat()
eigvec = cx_fmat()

eig_sym(eigval, eigvec, B)


# for matrices with complex elements

C =cx_fmat(50, 50, fill.randu)
D = C.t()*C

eigval2 = fmat()
eigvec2 = cx_fmat()

eig_sym(eigval2, eigvec2, D)

#eig_gen
A = cx_fmat(10, 10, fill.randu)

eigval = fmat()
eigvec = cx_fmat()

eig_gen(eigval, eigvec, A)
eig_gen(eigval, eigvec, A, "balance")

#eig_pair
A = cx_fmat(10, 10, fill.randu)
B = cx_fmat(10, 10, fill.randu)

eigval = fmat()
eigvec = cx_fmat()

eig_pair(eigval, eigvec, A, B)

#hess
X = cx_fmat(20,20, fill.randu)

U = cx_fmat()
H = cx_fmat()

hess(U, H, X)

#inv
A = cx_fmat(5, 5, fill.randu)

B = inv(A)

#inv_sympd
A = cx_fmat(5, 5, fill.randu)
B = A.t() * A
C = inv_sympd(B)

#lu
A = cx_fmat(5, 5, fill.randu)

L = cx_fmat()
U = cx_fmat()
P = cx_fmat()

lu(L, U, P, A)

B = P.t()*L*U

#null
A = cx_fmat(5, 6, fill.randu)

A[0,:].zeros()
A[:,0].zeros()

B = null(A)

#orth
A = cx_fmat(5, 6, fill.randu)

B = orth(A)

#pinv
A = cx_fmat(4, 5, fill.randu)

B = pinv(A)        # use default tolerance

C = pinv(A, 0.01)  # set tolerance to 0.01

#qr
X = cx_fmat(5, 5, fill.randu)

Q = cx_fmat()
R = cx_fmat()

qr(Q, R, X)

P_vec = umat()
P_mat = umat()

qr(Q, R, P_vec, X, "vector")
qr(Q, R, P_mat, X, "matrix")

#qr_econ
X = cx_fmat(6, 5, fill.randu)

Q = cx_fmat()
R = cx_fmat()

qr_econ(Q, R, X)

#qz
A = cx_fmat(10, 10, fill.randu)
B = cx_fmat(10, 10, fill.randu)

AA = cx_fmat()
BB = cx_fmat()
Q = cx_fmat()
Z = cx_fmat() 

qz(AA, BB, Q, Z, A, B)

#schur
X = cx_fmat(20,20, fill.randu)

U = cx_fmat()
S = cx_fmat()

schur(U, S, X)

#solve
A = cx_fmat(5, 5, fill.randu)
b = cx_fmat(5, 1, fill.randu)
B = cx_fmat(5, 5, fill.randu)

x1 = solve(A, b)

x2 = cx_fmat()
status = solve(x2, A, b)

X1 = solve(A, B)

X2 = solve(A, B, solve_opts.fast)  # enable fast mode

#svd
X = cx_fmat(5, 5, fill.randu)

U = cx_fmat()
s = fmat()
V = cx_fmat()

svd(U,s,V,X)

#svd_econ
X = cx_fmat(4, 5, fill.randu)

U = cx_fmat()
s = fmat()
V = cx_fmat()

svd_econ(U, s, V, X)

#syl
A = cx_fmat(5, 5, fill.randu)
B = cx_fmat(5, 5, fill.randu)
C = cx_fmat(5, 5, fill.randu)

X1 = syl(A, B, C)

X2 = cx_fmat()
syl(X2, A, B, C)

#sigproc
#conv
A = cx_fmat(256, 1, fill.randu)

B = cx_fmat(16, 1, fill.randu)

C = conv(A, B)

D = conv(A, B, "same")

#conv2
A = cx_fmat(256, 256, fill.randu)

B = cx_fmat(16, 16, fill.randu)

C = conv2(A, B)

D = conv2(A, B, "same")

#fft
X = cx_fmat(100, 1, fill.randu)
  
Y = fft(X, 128)

#fft2
A = cx_fmat(100, 100, fill.randu)
  
B = fft2(A)
C = fft2(A, 128, 128)

# #interp1
# x = linspace(0, 3, 20)
# y = square(x)

# xx = linspace(0, 3, 100)

# yy = cx_fmat()

# interp1(x, y, xx, yy)  # use linear interpolation by default

# interp1(x, y, xx, yy, "*linear")  # faster than "linear"

# interp1(x, y, xx, yy, "nearest")

# #interp2
# Z = cx_fmat()

# Z.load("tests_doc/input_image.pgm", pgm_binary)  # load an image in pgm format

# X = regspace(1, Z.n_cols)  # X = horizontal spacing
# Y = regspace(1, Z.n_rows)  # Y = vertical spacing

# XI = regspace(X.min(), 1.0/2.0, X.max()) # magnify by approx 2
# YI = regspace(Y.min(), 1.0/3.0, Y.max()) # magnify by approx 3

# ZI = cx_fmat()

# interp2(X, Y, Z, XI, YI, ZI)  # use linear interpolation by default

# ZI.save("output_image.pgm", pgm_binary)

#polyfit
x = linspace(0,4*datum.pi,100)
y = cos(x)

p = polyfit(x,y,10)

#polyval
x1 = linspace(0,4*datum.pi,100)
y1 = cos(x1)
p1 = polyfit(x1,y1,10)

y2 = polyval(p1,x1)

#stats
A = cx_fmat(5, 5, fill.randu)

B = mean(A)
C = var(A)
m = mean(mean(A))

v = cx_fmat(5, 1, fill.randu)
x = var(v)

#cov
X = cx_fmat(4, 5, fill.randu)
Y = cx_fmat(4, 5, fill.randu)

C = cov(X,Y)
D = cov(X,Y, 1)

#cor
X = cx_fmat(4, 5, fill.randu)
Y = cx_fmat(4, 5, fill.randu)

R = cor(X,Y)
S = cor(X,Y, 1)

# #hist
# v = cx_fmat(1000, 1, fill.randn) # Gaussian distribution

# h1 = hist(v, 11)
# h2 = hist(v, linspace(-2,2,11))

# #histc
# v = cx_fmat(1000, 1, fill.randn)  # Gaussian distribution

# h = histc(v, linspace(-2,2,11))

# #quantile
# V = cx_fmat(1000, 1, fill.randn)  # Gaussian distribution

# P = cx_fmat([ 0.25, 0.50, 0.75 ])

# Q = quantile(V, P)

#princomp
A = cx_fmat(5, 4, fill.randu)

coeff = cx_fmat()
score = cx_fmat()
latent = fmat()
tsquared = cx_fmat()

princomp(coeff, score, latent, tsquared, A)

# #normpdf
# X = cx_fmat(10, 1, fill.randu)
# M = cx_fmat(10, 1, fill.randu)
# S = cx_fmat(10, 1, fill.randu)

# P1 = normpdf(X)
# P2 = normpdf(X,    M,    S   )
# P3 = normpdf(1.23, M,    S   )
# P4 = normpdf(X,    4.56, 7.89)
# P5 = normpdf(1.23, 4.56, 7.89)

# #log_normpdf
# X = cx_fmat(10, 1, fill.randu)
# M = cx_fmat(10, 1, fill.randu)
# S = cx_fmat(10, 1, fill.randu)

# P1 = log_normpdf(X)
# P2 = log_normpdf(X,    M,    S   )
# P3 = log_normpdf(1.23, M,    S   )
# P4 = log_normpdf(X,    4.56, 7.89)
# P5 = log_normpdf(1.23, 4.56, 7.89)

# #normcdf
# X = cx_fmat(10, 1, fill.randu)
# M = cx_fmat(10, 1, fill.randu)
# S = cx_fmat(10, 1, fill.randu)

# P1 = normcdf(X)
# P2 = normcdf(X,    M,    S   )
# P3 = normcdf(1.23, M,    S   )
# P4 = normcdf(X,    4.56, 7.89)
# P5 = normcdf(1.23, 4.56, 7.89)

# #mvnrnd
# M = cx_fmat(5, 1, fill.randu)

# B = cx_fmat(5, 5, fill.randu)
# C = B.t() * B

# X = mvnrnd(M, C, 100)

# #chi2rnd
# from random import randint
# X = chi2rnd(2, 5, 6)

# A = cx_fmat(5, 6)
# A.imbue(lambda: randint(1,10)) # imbue with random integers
# B = chi2rnd(A)

# #wishrnd
# X = cx_fmat(5, 5, fill.randu)

# S = X.t() * X

# W = wishrnd(S, 6.7)

# #iwishrnd
# X = cx_fmat(5, 5, fill.randu)

# T = X.t() * X

# W = iwishrnd(T, 6.7)

#running_stat
from random import normalvariate
import builtins
stats = cx_frunning_stat()

for i in builtins.range(10000):
  sample = normalvariate(0, 1) # normal distribution
  stats(sample)

print("mean = " + str(stats.mean()))
print("var  = " + str(stats.var()))
print("min  = " + str(stats.min()))
print("max  = " + str(stats.max()))

#running_stat_vec
import builtins
stats = cx_frunning_stat_vec()

for i in builtins.range(10000):
  sample = cx_fmat(5, 1, fill.randu)
  stats(sample)

stats.mean().print("mean = ")
stats.var().print("var  = ")
stats.max().print("max  = ")

more_stats = cx_frunning_stat_vec(True)

for i in builtins.range(20):
  sample = cx_fmat(1, 3, fill.randu)
  
  sample[1] -= sample[0]
  sample[2] += sample[1]
  
  more_stats(sample)

more_stats.cov().print("covariance matrix = ")

sd = more_stats.stddev()

(more_stats.cov() / (sd.t() * sd)).print("correlations = ")

#kmeans
# d = 5       # dimensionality
# N = 10000   # number of vectors

# data = cx_fmat(d, N, fill.randu)

# means = cx_fmat()

# status = kmeans(means, data, 2, random_subset, 10, True)

# if not status:
#   print("clustering failed")

# means.print("means:")

#const
print("2.0 * pi = " + str(2.0 * datum.pi))

print("speed of light = " + str(datum.c_0))

print("log_max for floats = " + str(fdatum.log_max))

print("log_max for doubles = " + str(datum.log_max))

#wall_clock
import builtins
timer = wall_clock()

A = cx_fmat(100, 100, fill.randu)
B = cx_fmat(100, 100, fill.randu)
C = cx_fmat()

timer.tic()

for i in builtins.range(100000):
  C = A + B + A + B

n = timer.toc()

print("number of seconds: " + str(n))

#libs
libraries()

#ex
A = cx_fmat(4, 5, fill.randu)
B = cx_fmat(4, 5, fill.randu)
  
(A*B.t()).print()