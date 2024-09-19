clc;clearvars;

A = [2, 1, 1; 4, 4, 1; 6, -5, 8];
b = [4; 7; 15];

A = [1 -1; 2 -3];
b = [10; -6];

A = [4 1 -1; 5 1 2; 6 1 1];
b = [-2; 4; 6];

A = [4, 1, -1; 2, 7, 1; 1, -3, 12];
b = [3; 19; 31];

% r will serve as the total number of iterations.
[r, c] = size(A);

if r ~= c, error("Gauss elimination works for square matrices only.")
end

L = diag(ones(1, r));
U = A;

% Forward Elimination
for i=1:r
    for j=i+1:r
        factor = (U(j, i) / U(i, i));
        tr_vec = U(i, :) .* factor;
        U(j, :) = U(j, :) - tr_vec;
        L(j, i) = factor;
    end
end

unknown_z_vars = zeros(r, 1);

% Forward Substitution
for i=1:r
    x = 0;
    for j=1:r
        x = x + L(i, j) * unknown_z_vars(j, 1);
    end
    x = (b(i) - x)/ L(i, i);
    unknown_z_vars(i, 1) = x;
end

z = unknown_z_vars;

unknown_x_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = sum(U(i, :)' .* unknown_x_vars); 
    x = (z(i) - x)/ U(i, i);
    unknown_x_vars(i, 1) = x;
end

disp(unknown_x_vars)

