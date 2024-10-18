clc;clearvars;

A = [0.3 0.52 1.0; 0.5 1.0 1.9; 0.1 0.3 0.5];
b = [-0.01; 0.67; -0.44];

A = [4 1 -1; 2 7 1; 1 -3 12];
b = [3; 19; 31];

% disp(cramers_rule(A, b))
% disp(gauss_elimination(A, b))
% disp(gauss_jacobi(A, b))
% disp(gauss_seidel(A, b))
% disp(lu_decomposition(A, b)) 
% disp(gauss_jordan(A, b))
disp(mat_inv(A) * A)
