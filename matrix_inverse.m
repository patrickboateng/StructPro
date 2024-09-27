clc;clearvars;

% Calculating the inverse of a matrix using LU decomposition

A = [3, -0.1, -0.2; 0.1, 7, -0.3; 0.3, -0.2, 10];

% A = [2, 1; 2, 2];

% r will serve as the total number of iterations.
[r, c] = size(A);

if r ~= c, error("Gauss elimination works for square matrices only.")
end

% Lower triangular matrix
L = diag(ones(1, r));
% Upper triangular matrix
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

I = eye(r);

invMat = zeros(r);

for i=1:r

    b = I(:, i);
    unknown_z_vars = zeros(r, 1);

    % Forward elimination
    for j=1:r
        x = L(j, :) * unknown_z_vars;
        x = (b(j) - x) / L(j, j);
        unknown_z_vars(j, 1) = x;
    end
   
    unknown_x_vars = zeros(r, 1);

    % Backward elimination
    for k=r:-1:1
        x = U(k, :) * unknown_x_vars;
        x = (unknown_z_vars(k) - x) / U(k, k);
        unknown_x_vars(k, 1) = x;
    end

    invMat(:, i) = unknown_x_vars;

end

disp(invMat);
