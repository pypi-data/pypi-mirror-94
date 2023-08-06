from pyarma import *

# umat class
A = umat(5, 5, fill.randu)
x = A[1,2]

M = umat(5, 5, fill.ones) # initialise 5x5 matrix with ones
N = umat(M)                # convert to double-precision floating point

B = A + A
C = A * B
D = A @ B

# X = cx_mat(A,B)

B.zeros()
B.set_size(10,10)
B.ones(5,6)

B.print("B:")

# Operations
A = umat(5, 10, fill.randu)
B = umat(5, 10, fill.randu)
C = umat(10, 5, fill.randu)

P = A + B
Q = A - B
R = -B
S = A / 123
T = A @ B
U = A * C

AA = umat("1 2 3; 4 5 6; 7 8 9;")
BB = umat("3 2 1; 6 5 4; 9 8 7;")

# compare elements
ZZ = (AA >= BB)

# broadcasting
X = umat(6, 5, fill.ones)
v = umat(6, 1, fill.randu)

# in-place addition of v to each column vector of X
X += v

# generate Y by adding v to each column vector of X
Y = X + v 

# attributes
X = umat(4,5)
print("X has " + str(X.n_cols) + " columns")

# indexing
A = umat(10, 10, fill.randu)
A[9,9] = 123
x = A[9,9]
y = A[99]

# element initialisation
v = umat([ 1, 2, 3 ])
A = umat([ [1, 3, 5],
          [2, 4, 6] ])

# member zeros
A = umat(5,10)
A.zeros()   
# or:  A = umat(5,10,fill.zeros)

B = umat()
B.zeros(10,20)

C = umat()
C.zeros( size(B) )

# member ones
A = umat(5,10)
A.ones()
# or:  A = umat(5,10,fill.ones)

B = umat()
B.ones(10,20)

C = umat()
C.ones( size(B) )

# member eye
A = umat(5,5)
A.eye()
# or:  A = umat(5,5,fill.eye)

B = umat()
B.eye(5,5)

C = umat()
C.eye( size(B) )

# randu/randn
A = umat(5,10)
A.randu()
# or:  A = umat(5,10,fill.randu)

B = umat()
B.randu(10,20)

C = umat()
C.randu( size(B) )

pyarma_rng.set_seed_random()  # set the seed to a random value

# fill
A = umat(5, 6)
A.fill(123)
# A.fill(123) is also accepted and has the same result
A = umat(5, 6, fill.zeros)

#imbue
from random import randint
  
A = umat(4, 5)
  
A.imbue( lambda: randint(0,9) )

# clean
A = umat()

A.randu(1000, 1000)

A[12,34] =  123
A[56,78] = 123

A.clean(123)

# replace
import math
A = umat(5, 6, fill.randu)

A[diag].fill(111)

A.replace(111, 0) # replace each NaN with 0

#transform
A = umat(4, 5, fill.ones)

# add 123 to every element
A.transform( lambda val: val + 123 )

# for_each
# print each element in a dense matrix

A = umat(4, 5, fill.ones)

A.for_each( lambda val: print(val) )

# set_size
A = umat()
A.set_size(5,10)       # or:  A = umat(5,10)

B = umat()
B.set_size( size(A) )  # or:  B = umat( size(A) )

# reshape
A = umat(4, 5, fill.randu)

A.reshape(5,4)

# resize
A = umat(4, 5, fill.randu)

A.resize(7,6)

# copy_size

A = umat(5, 6, fill.randu)
B = umat()
B.copy_size(A)

# reset
A = umat(5, 5, fill.randu)
A.reset()

print(str(B.n_rows))
print(str(B.n_cols))

# reset
A = umat(5, 5, fill.randu)
A.reset()

# submatrix
A = umat(5, 10, fill.zeros)

A[ 0:2, 1:3 ]             = umat(3,3, fill.randu)
# A[ span(0,2), span(1,3) ] = umat(3,3, fill.randu)
# A[ 0,1, size(3,3) ]       = umat(3,3, fill.randu)

B = A[ 0:2, 1:3 ].eval()
# C = A[ span(0,2), span(1,3) ].eval()
# D = A[ 0,1, size(3,3) ].eval()

A[:,1]          = umat(5,1,fill.randu)
# A[span_all, 1]  = umat(5,1,fill.randu)

X = umat(5, 5, fill.randu)

# get all elements of X that are greater than 0
q = X[ find(X > 0) ]

# add 123 to all elements of X greater than 0
X[ find(X > 0) ] += 123

# set four specific elements of X to 1
indices = umat([ 2, 3, 6, 8 ])

X[indices] = umat(4,1,fill.ones)

# diagonal
X = umat(5, 5, fill.randu)

a = X[diag]
b = X[diag, 1]
c = X[diag, -2]

X[diag] = umat(5,1,fill.randu)
X[diag] += 6
X[diag].ones()

# set_real, set_imag
A = umat(4, 5, fill.randu)
B = umat(4, 5, fill.randu)

C = cx_mat(4, 5, fill.zeros)

C.set_real(A)
C.set_imag(B)

# fast cx_mat
A = umat(4, 5, fill.randu)
B = umat(4, 5, fill.randu)

# C = cx_mat(A,B)

# ins_row/cols
A = umat(5, 10, fill.randu)
B = umat(5,  2, fill.ones )

# at column 2, insert a copy of B;
# A will now have 12 columns
A.insert_cols(2, B)

# at column 1, insert 5 zeroed columns;
# B will now have 7 columns
B.insert_cols(1, 5)

# shed_row/cols
A = umat(5, 10, fill.randu)
B = umat(5, 10, fill.randu)

A.shed_row(2)
A.shed_cols(2,4)

indices = umat([4, 6, 8])
B.shed_cols(indices)

#swap_rows
X = umat(5, 5, fill.randu)
X.swap_rows(0,4)

# swap
A = umat(4, 5, fill.zeros)
B = umat(6, 7, fill.ones )

A.swap(B)

# iterators
X = umat(5, 6, fill.randu)

for i in X:                # this prints all elements
  print(i)

it = iter(X)               # this also prints all elements
for i in it:
  print(i)

col_it = col_iter(X, 1, 3) # start of column 1 and end of column 3

for i in col_it:
  print(i)

# iterators for submats
X = umat(100, 200, fill.randu)

for val in X[40:60, 50:100]:
  print(val)

# as_col
X = umat(4, 5, fill.randu)
v = X.as_col()

#trans
A = umat(4, 5, fill.randu)
B = A.t()

# #inv
# A = umat(4, 4, fill.randu)

# X = A.i()

# Y = (A+A).i()

#max
A = umat(5, 5, fill.randu)

max_val = A.max()

#ind_max
A = umat(5, 5, fill.randu)

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
A = umat(4, 5, fill.randu)

print(A.in_range(0,0))  # true
print(A.in_range(3,4))  # true
print(A.in_range(4,5))  # false

#is_empty
A = umat(5, 5, fill.randu)
print(A.is_empty())

A.reset()
print(A.is_empty())


#is_vec
A = umat(1, 5, fill.randu)
B = umat(5, 1, fill.randu)
C = umat(5, 5, fill.randu)

print(A.is_vec())
print(B.is_vec())
print(C.is_vec())

#is_sorted
a = umat(10, 1, fill.randu)
b = sort(a)

check1 = a.is_sorted()
check2 = b.is_sorted()

A = umat(10, 10, fill.randu)

# check whether each column is sorted in descending manner
print(A.is_sorted("descend"))

# check whether each row is sorted in ascending manner
print(A.is_sorted("ascend", 1))

# is_trimatu/l
A = umat(5, 5, fill.randu)
B = trimatl(A)

print(A.is_trimatu())
print(B.is_trimatl())

#is_diagmat
A = umat(5, 5, fill.randu)
B = diagmat(A)

print(A.is_diagmat())
print(B.is_diagmat())

#is_square
A = umat(5, 5, fill.randu)
B = umat(6, 7, fill.randu)

print(A.is_square())
print(B.is_square())

#is_symm
A = umat(5, 5, fill.randu)
B = A.t() * A

print(A.is_symmetric())
print(B.is_symmetric())

#is_hermitian
cx_A = cx_mat(5, 5, fill.randu)
cx_B = A.t() * A

print(A.is_hermitian())
print(B.is_hermitian())

# #is_sympd
# A = umat(5, 5, fill.randu)

# B = A.t() * A

# print(A.is_sympd())
# print(B.is_sympd())

#is_zero
A = umat(5, 5, fill.zeros)

# A[0,0] = datum.eps

print(A.is_zero())
# print(A.is_zero(datum.eps))

#is_finite
A = umat(5, 5, fill.randu)
B = umat(5, 5, fill.randu)

B = umat(1,1)
# B[0,0] = datum.inf

print(A.is_finite())
print(B.is_finite())

#has_inf
A = umat(5, 5, fill.randu)
B = umat(5, 5, fill.randu)

B = umat(1,1)
# B[0,0] = datum.inf

print(A.has_inf())
print(B.has_inf())

#has_nan
A = umat(5, 5, fill.randu)
B = umat(5, 5, fill.randu)

B = umat(1,1)
# B[0,0] = datum.nan
# 
print(A.has_nan())
print(B.has_nan())

#print
A = umat(5, 5, fill.randu)
B = umat(6, 6, fill.randu)

A.print()

# print a transposed version of A
A.t().print()

# "B:" is the optional header line
B.print("B:")

#save/load
A = umat(5, 6, fill.randu)

# default save format is arma_binary
A.save("A.bin")

# save in raw_ascii format
A.save("A.txt", raw_ascii)

# save in CSV format without a header
A.save("A.csv", csv_ascii)

# save in HDF5 format
# A.save("A.h5", hdf5_binary)

# automatically detect format type while loading
B = umat()
B.load("A.bin")

# force loading in arma_ascii format
C = umat()
C.load("A.txt", arma_ascii)

# example of testing for success
D = umat()
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
A = umat(5, 1, fill.randu)
X = toeplitz(A)
Y = circ_toeplitz(A)

# abs
A = umat(5, 5, fill.randu)
B = abs(A) 

X = cx_mat(5, 5, fill.randu)
Y = abs(X)

# accu
A = umat(5, 6, fill.randu)
B = umat(5, 6, fill.randu)

x = accu(A)

y = accu(A @ B)

# accu(A @ B) is a "multiply-and-accumulate" operation
# as operator @ performs element-wise multiplication

#all
V = umat(10,1, fill.randu)
X = umat(5, 5, fill.randu)

# status1 will be set to true if vector V has all non-zero elements
status1 = all(V)

# status2 will be set to true if vector V has all elements greater than 0
status2 = all(V > 0)

# status3 will be set to true if matrix X has all elements greater than 0;
# note the use of vectorise()
status3 = all(vectorise(X) > 0)

# generate a row vector indicating which columns of X have all elements greater than 0
uA = all(X > 0)

#any
V = umat(10,1, fill.randu)
X = umat(5, 5, fill.randu)

# status1 will be set to true if vector V has any non-zero elements
status1 = any(V)

# status2 will be set to true if vector V has any elements greater than 0
status2 = any(V > 0)

# status3 will be set to true if matrix X has any elements greater than 0;
# note the use of vectorise()
status3 = any(vectorise(X) > 0)

# generate a row vector indicating which columns of X have elements greater than 0
uA = any(X > 0)

#approx_equal
A = umat(5, 5, fill.randu)
B = A + 0

same1 = approx_equal(A, B, "absdiff", 0)

C = 1000 * umat(5,5, fill.randu)
D = C + 1

same2 = approx_equal(C, D, "reldiff", 0)

same3 = approx_equal(C, D, "both", 2, 0)

#arg
A = cx_mat(5, 5, fill.randu)
B = arg(A)

#as_scalar
r = umat(1, 5, fill.randu)
q = umat(5, 1, fill.randu)

X = umat(5, 5, fill.randu)

a = as_scalar(r*q)
b = as_scalar(r*X*q)
c = as_scalar(r*diagmat(X)*q)
# d = as_scalar(r*inv(diagmat(X))*q)

#clamp
A = umat(5, 5, fill.randu )

B = clamp(A, 0,     0) 

C = clamp(A, A.min(), 0) 

D = clamp(A, 0, A.max()) 

#cond
A = umat(5, 5, fill.randu)
c = cond(A)

#conj
X = cx_mat(5, 5, fill.randu)
Y = conj(X)

#cross
a = umat(3, 1, fill.randu)
b = umat(3, 1, fill.randu)

c = cross(a,b)

#cumsum
A = umat(5, 5, fill.randu)
B = cumsum(A)
C = cumsum(A, 1)

x = umat(10, 1, fill.randu)
y = cumsum(x)

#cumprod
A = umat(5, 5, fill.randu)
B = cumprod(A)
C = cumprod(A, 1)

x = umat(10, 1, fill.randu)
y = cumprod(x)

#det
A = umat(5, 5, fill.randu)

x = det(A)

#diagmat
A = umat(5, 5, fill.randu)
B = diagmat(A)
C = diagmat(A,1)

v = umat(5, 1, fill.randu)
D = diagmat(v)
E = diagmat(v,1)

#diagvec
A = umat(5, 5, fill.randu)

d = diagvec(A)

#diff
a = linspace(1,10,10)

b = diff(a)

#dot
a = umat(10, 1, fill.randu)
b = umat(10, 1, fill.randu)

x = dot(a,b)

#eps
A = umat(4, 5, fill.randu)
B = eps(A)

#expmat
A = umat(5, 5, fill.randu)

B = expmat(A)

#expmat_sym
A = umat(5, 5, fill.randu)

B = A*A.t()   # make symmetric matrix

C = expmat_sym(B)

#find
A = umat(5, 5, fill.randu)
B = umat(5, 5, fill.randu)

q1 = find(A > B)
q2 = find(A > 0)
q3 = find(A > 0, 3, "last")

# change elements of A greater than 0 to 1
A[ find(A > 0) ].ones()

#find_finite
A = umat(5, 5, fill.randu)

# A[1,1] = datum.inf

# accumulate only finite elements
val = accu( A[ find_finite(A) ] )

#find_nonfinite
A = umat(5, 5, fill.randu)

# A[1,1] = datum.inf
# A[2,2] = datum.nan

# change non-finite elements to zero
A[ find_nonfinite(A) ].zeros()

#find_unique
A = umat([ [ 2, 2, 4 ], 
          [ 4, 6, 6 ] ])

indices = find_unique(A)

#fliplr/ud
A = umat(5, 5, fill.randu)

B = fliplr(A)
C = flipud(A)

#imag/real
C = cx_mat(5, 5, fill.randu)

A = imag(C)
B = real(C)

#ind2sub
M = umat(4, 5, fill.randu)

s = ind2sub( size(M), 6 )

print("row: " + str(s[0]))
print("col: " + str(s[1]))


indices = find(M > 0)
t       = ind2sub( size(M), indices )

#index_min/max

v = umat(10, 1, fill.randu)

i = index_max(v)
max_val_in_v = v[i]


M = umat(5, 6, fill.randu)

ii = index_max(M)
jj = index_max(M,1)

max_val_in_col_2 = M[ ii[2], 2 ]

max_val_in_row_4 = M[ 4, jj[4] ]

#inplace_trans
X = umat(4,     5,     fill.randu)
Y = umat(20, 30, fill.randu)

inplace_trans(X)

inplace_trans(Y)

#intersect
A = regspace(4, 1)  # 4, 3, 2, 1
B = regspace(3, 6)  # 3, 4, 5, 6

C = intersect(A,B)       # 3, 4

CC = umat()
iA = umat()
iB = umat()

intersect(CC, iA, iB, A, B)

#join
A = umat(4, 5, fill.randu)
B = umat(4, 6, fill.randu)
C = umat(6, 5, fill.randu)

AB = join_rows(A,B)
AC = join_cols(A,C)

#kron
A = umat(4, 5, fill.randu)
B = umat(5, 4, fill.randu)

K = kron(A,B)

#log_det
A = umat(5, 5, fill.randu)
result = log_det(A)

# #logmat
# A = umat(5, 5, fill.randu)

# B = logmat(A)

#logmat_sympd
A = umat(5, 5, fill.randu)

B = A*A.t()   # make symmetric matrix

C = logmat_sympd(B)

#max
v = umat(10, 1, fill.randu)
x = max(v)

M = umat(10, 10, fill.randu)

a = max(M)
b = max(M,0) 
c = max(M,1)

# element-wise maximum
X = umat(5, 6, fill.randu)
Y = umat(5, 6, fill.randu)
Z = max(X,Y)

#nonzeros
B = umat(100, 100, fill.eye)
b = nonzeros(B)

#norm
q = umat(5, 1, fill.randu)

x = norm(q, 2)
y = norm(q, "inf")

#normalise
A = umat(10, 1, fill.randu)
B = normalise(A)
C = normalise(A, 1)

X = umat(5, 6, fill.randu)
Y = normalise(X)
Z = normalise(X, 2, 1)

#print
A = umat(123, 456, fill.randu)

print(A)

# possible output:
# 
# <pyarma.pyarma.umat object at 0x123456>
# [matrix size: 123x456]
#    0   0   0      ...   0
#    0   0   0      ...   0
#    0   0   0      ...   0
#         :        :        :        :        :        
#    0   0   0      ...   0

#prod
v = umat(10, 1, fill.randu)
x = prod(v)

M = umat(10, 10, fill.randu)

a = prod(M)
b = prod(M,0)
c = prod(M,1)

#powmat
A = umat(5, 5, fill.randu)

B = powmat(A, 4)     #     integer exponent

# C = powmat(A, 4)  # non-integer exponent

#rank
A = umat(4, 5, fill.randu)

r = rank(A)

#rcond
A = umat(5, 5, fill.randu)

r = rcond(A)

#repelem
A = umat(2, 3, fill.randu)

B = repelem(A, 4, 5)

#repmat
A = umat(2, 3, fill.randu)

B = repmat(A, 4, 5)

#reshape
A = umat(10, 5, fill.randu)

B = reshape(A, 5, 10)

#resize
A = umat(4, 5, fill.randu)

B = resize(A, 7, 6)

#reverse
v = umat(123, 1, fill.randu)
y = reverse(v)

A = umat(4, 5, fill.randu)
B = reverse(A)
C = reverse(A,1)

#roots
P = umat(5, 1, fill.randu)
  
R = roots(P)

#shift
A = umat(4, 5, fill.randu)
B = shift(A, -1)
C = shift(A, +1)

#size
A = umat(5,6)

B = umat(size(A), fill.zeros)

C = umat()

C.randu(size(A))

D = umat(10,20, fill.ones)
D[3,4,size(C)] = C    # access submatrix of E

E = umat( size(A) + size(E) )
G = umat( size(A) * 2 )
print("size of A: " + str(size(A)))
is_same_size = (size(A) == size(E))

#shuffle
A = umat(4, 5, fill.randu)
B = shuffle(A)

#sort
A = umat(10, 10, fill.randu)
B = sort(A)

#sort_index
q = umat(10, 1, fill.randu)

indices = sort_index(q)

# #sqrtmat
# A = umat(5, 5, fill.randu)

# B = sqrtmat(A)

#sqrtmat_sympd
A = umat(5, 5, fill.randu)

B = A*A.t()   # make symmetric matrix

C = sqrtmat_sympd(B)

#sum
v = umat(10, 1, fill.randu)
x = sum(v)

M = umat(10, 10, fill.randu)

a = sum(M)
b = sum(M,0)
c = sum(M,1)

y = accu(M)   # find the overall sum regardless of object type

#sub2ind
M = umat(4,5)

i = sub2ind( size(M), 2, 3 )

#symmat
A = umat(5, 5, fill.randu)

B = symmatu(A)
C = symmatl(A)

#trace
A = umat(5, 5, fill.randu)

x = trace(A)

#trans
A = umat(5, 10, fill.randu)

B = trans(A)
C = A.t()    # equivalent to trans(A), but more compact

#trapz
X = linspace(0, datum.pi, 1000)
Y = sin(X)

Z = trapz(X,Y)

#trimat
A = umat(5, 5, fill.randu)

U  = trimatu(A)
L  = trimatl(A)

UU = trimatu(A,  1)  # omit the main diagonal
LL = trimatl(A, -1)  # omit the main diagonal

#trimat_ind
A = umat(5, 5, fill.randu)

upper_indices = trimatu_ind( size(A) )
lower_indices = trimatl_ind( size(A) )

# extract upper/lower triangle into vector
upper_part = A[upper_indices]
lower_part = A[lower_indices]

# obtain indices without the main diagonal
alt_upper_indices = trimatu_ind( size(A),  1)
alt_lower_indices = trimatl_ind( size(A), -1)

#unique
X = umat([ [ 1, 2 ],
          [ 2, 3 ] ])
Y = unique(X)

#vectorise
X = umat(4, 5, fill.randu)

v = vectorise(X)

#exp
A = umat(5, 5, fill.randu)
B = exp(A)

#cos
X = umat(5, 5, fill.randu)
Y = cos(X)

#chol
X = umat(5, 5, fill.randu)
Y = X.t()*X

R1 = chol(Y)
R2 = chol(Y, "lower")

#eig_sym
# for matrices with real elements

A = umat(50, 50, fill.randu)
B = A.t()*A  # generate a symmetric matrix

eigval = umat()
eigvec = umat()

eig_sym(eigval, eigvec, B)


# for matrices with complex elements

C =cx_mat(50, 50, fill.randu)
D = C.t()*C

eigval2 = umat()
eigvec2 = cx_mat()

eig_sym(eigval2, eigvec2, D)

#eig_gen
A = umat(10, 10, fill.randu)

eigval = cx_mat()
eigvec = cx_mat()

eig_gen(eigval, eigvec, A)
eig_gen(eigval, eigvec, A, "balance")

#eig_pair
A = umat(10, 10, fill.randu)
B = umat(10, 10, fill.randu)

eigval = cx_mat()
eigvec = cx_mat()

eig_pair(eigval, eigvec, A, B)

#hess
X = umat(20,20, fill.randu)

U = umat()
H = umat()

hess(U, H, X)

#inv
A = umat(5, 5, fill.randu)

B = inv(A)

#inv_sympd
A = umat(5, 5, fill.randu)
B = A.t() * A
C = inv_sympd(B)

#lu
A = umat(5, 5, fill.randu)

L = umat()
U = umat()
P = umat()

lu(L, U, P, A)

B = P.t()*L*U

#null
A = umat(5, 6, fill.randu)

A[0,:].zeros()
A[:,0].zeros()

B = null(A)

#orth
A = umat(5, 6, fill.randu)

B = orth(A)

#pinv
A = umat(4, 5, fill.randu)

B = pinv(A)        # use default tolerance

C = pinv(A, 0)  # set tolerance to 0

#qr
X = umat(5, 5, fill.randu)

Q = umat()
R = umat()

qr(Q, R, X)

P_vec = umat()
P_mat = umat()

qr(Q, R, P_vec, X, "vector")
qr(Q, R, P_mat, X, "matrix")

#qr_econ
X = umat(6, 5, fill.randu)

Q = umat()
R = umat()

qr_econ(Q, R, X)

#qz
A = umat(10, 10, fill.randu)
B = umat(10, 10, fill.randu)

AA = umat()
BB = umat()
Q = umat()
Z = umat() 

qz(AA, BB, Q, Z, A, B)

#schur
X = umat(20,20, fill.randu)

U = umat()
S = umat()

schur(U, S, X)

#solve
A = umat(5, 5, fill.randu)
b = umat(5, 1, fill.randu)
B = umat(5, 5, fill.randu)

x1 = solve(A, b)

x2 = umat()
status = solve(x2, A, b)

X1 = solve(A, B)

X2 = solve(A, B, solve_opts.fast)  # enable fast mode

#svd
X = umat(5, 5, fill.randu)

U = umat()
s = umat()
V = umat()

svd(U,s,V,X)

#svd_econ
X = umat(4, 5, fill.randu)

U = umat()
s = umat()
V = umat()

svd_econ(U, s, V, X)

#syl
A = umat(5, 5, fill.randu)
B = umat(5, 5, fill.randu)
C = umat(5, 5, fill.randu)

X1 = syl(A, B, C)

X2 = umat()
syl(X2, A, B, C)

#sigproc
#conv
A = umat(256, 1, fill.randu)

B = umat(16, 1, fill.randu)

C = conv(A, B)

D = conv(A, B, "same")

#conv2
A = umat(256, 256, fill.randu)

B = umat(16, 16, fill.randu)

C = conv2(A, B)

D = conv2(A, B, "same")

#fft
X = umat(100, 1, fill.randu)
  
Y = fft(X, 128)

#fft2
A = umat(100, 100, fill.randu)
  
B = fft2(A)
C = fft2(A, 128, 128)

#interp1
x = linspace(0, 3, 20)
y = square(x)

xx = linspace(0, 3, 100)

yy = umat()

interp1(x, y, xx, yy)  # use linear interpolation by default

interp1(x, y, xx, yy, "*linear")  # faster than "linear"

interp1(x, y, xx, yy, "nearest")

#interp2
Z = umat()

Z.load("tests_doc/input_image.pgm", pgm_binary)  # load an image in pgm format

X = regspace(1, Z.n_cols)  # X = horizontal spacing
Y = regspace(1, Z.n_rows)  # Y = vertical spacing

XI = regspace(X.min(), 1/2, X.max()) # magnify by approx 2
YI = regspace(Y.min(), 1/3, Y.max()) # magnify by approx 3

ZI = umat()

interp2(X, Y, Z, XI, YI, ZI)  # use linear interpolation by default

ZI.save("output_image.pgm", pgm_binary)

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
A = umat(5, 5, fill.randu)

B = mean(A)
C = var(A)
m = mean(mean(A))

v = umat(5, 1, fill.randu)
x = var(v)

#cov
X = umat(4, 5, fill.randu)
Y = umat(4, 5, fill.randu)

C = cov(X,Y)
D = cov(X,Y, 1)

#cor
X = umat(4, 5, fill.randu)
Y = umat(4, 5, fill.randu)

R = cor(X,Y)
S = cor(X,Y, 1)

# TODO: FIX THIS
# #hist
# v = umat(1000, 1, fill.randn) # Gaussian distribution

# h1 = hist(v, 11)
# h2 = hist(v, umat(linspace(-2,2,11)))

# #histc
# v = umat(1000, 1, fill.randn)  # Gaussian distribution

# h = histc(v, umat(linspace(-2,2,11)))

# #quantile
# V = umat(1000, 1, fill.randn)  # Gaussian distribution

# P = umat([ 0, 0, 0 ])

# Q = quantile(V, P)

# #princomp
# A = umat(5, 4, fill.randu)

# coeff = umat()
# score = umat()
# latent = umat()
# tsquared = umat()

# princomp(coeff, score, latent, tsquared, A)

# #normpdf
# X = umat(10, 1, fill.randu)
# M = umat(10, 1, fill.randu)
# S = umat(10, 1, fill.randu)

# P1 = normpdf(X)
# P2 = normpdf(X,    M,    S   )
# P3 = normpdf(1, M,    S   )
# P4 = normpdf(X,    4, 7)
# P5 = normpdf(1, 4, 7)

# #log_normpdf
# X = umat(10, 1, fill.randu)
# M = umat(10, 1, fill.randu)
# S = umat(10, 1, fill.randu)

# P1 = log_normpdf(X)
# P2 = log_normpdf(X,    M,    S   )
# P3 = log_normpdf(1, M,    S   )
# P4 = log_normpdf(X,    4, 7)
# P5 = log_normpdf(1, 4, 7)

# #normcdf
# X = umat(10, 1, fill.randu)
# M = umat(10, 1, fill.randu)
# S = umat(10, 1, fill.randu)

# P1 = normcdf(X)
# P2 = normcdf(X,    M,    S   )
# P3 = normcdf(1, M,    S   )
# P4 = normcdf(X,    4, 7)
# P5 = normcdf(1, 4, 7)

# #mvnrnd
# M = umat(5, 1, fill.randu)

# B = umat(5, 5, fill.randu)
# C = B.t() * B

# X = mvnrnd(M, C, 100)

# #chi2rnd
# from random import randint
# X = chi2rnd(2, 5, 6)

# A = umat(5, 6)
# A.imbue(lambda: randint(1,10)) # imbue with random integers
# B = chi2rnd(A)

# #wishrnd
# X = umat(5, 5, fill.randu)

# S = X.t() * X

# W = wishrnd(S, 6)

# #iwishrnd
# X = umat(5, 5, fill.randu)

# T = X.t() * X

# W = iwishrnd(T, 6)

# #running_stat
# from random import normalvariate
# import builtins
# stats = running_stat()

# for i in builtins.range(10000):
#   sample = normalvariate(0, 1) # normal distribution
#   stats(sample)

# print("mean = " + str(stats.mean()))
# print("var  = " + str(stats.var()))
# print("min  = " + str(stats.min()))
# print("max  = " + str(stats.max()))

# #running_stat_vec
# import builtins
# stats = running_stat_vec()

# for i in builtins.range(10000):
#   sample = umat(5, 1, fill.randu)
#   stats(sample)

# stats.mean().print("mean = ")
# stats.var().print("var  = ")
# stats.max().print("max  = ")

# more_stats = running_stat_vec(True)

# for i in builtins.range(20):
#   sample = umat(1, 3, fill.randu)
  
#   sample[1] -= sample[0]
#   sample[2] += sample[1]
  
#   more_stats(sample)

# more_stats.cov().print("covariance matrix = ")

# sd = more_stats.stddev()

# (more_stats.cov() / (sd.t() * sd)).print("correlations = ")

# #kmeans
# d = 5       # dimensionality
# N = 10000   # number of vectors

# data = umat(d, N, fill.randu)

# means = umat()

# status = kmeans(means, data, 2, random_subset, 10, True)

# if not status:
#   print("clustering failed")

# means.print("means:")

#const
print("2 * pi = " + str(2 * datum.pi))

print("speed of light = " + str(datum.c_0))

print("log_max for floats = " + str(fdatum.log_max))

print("log_max for doubles = " + str(datum.log_max))

#wall_clock
import builtins
timer = wall_clock()

A = umat(100, 100, fill.randu)
B = umat(100, 100, fill.randu)
C = umat()

timer.tic()

for i in builtins.range(100000):
  C = A + B + A + B

n = timer.toc()

print("number of seconds: " + str(n))

#libs
libraries()

#ex
A = umat(4, 5, fill.randu)
B = umat(4, 5, fill.randu)
  
(A*B.t()).print()