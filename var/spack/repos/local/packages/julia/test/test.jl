using LinearAlgebra
H = [1 2im;
     -2im 1]
A = [-4 0 6;
     -3 2 3;
     -3 0 5]
println(eigen(A).values)
println(eigvals(H))

