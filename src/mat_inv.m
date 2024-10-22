% Calculating the inverse of a matrix using LU decomposition
function invMat = mat_inv(A)
arguments
    A (:, :) {mustBeMatrix}
end
% r will serve as the total number of iterations.
[r, c] = size(A);

% Lower triangular matrix
L = eye(r);

tol = 1e-6;

% Forward Elimination
for i=1:r
    % find pivot and swap if zero or close to zero.
    A = swap(A, pv_idx=i, total_rows=r, TOL=tol);

    for j=i+1:r
        factor = (A(j, i) / A(i, i));
        A(j, :) = A(j, :) - A(i, :) .* factor;
        L(j, i) = factor;
    end
end

I = eye(r);
invMat = zeros(r, c);

for i=1:r
    b = I(:, i);
    unknown_z_vars = zeros(r, 1);

    % Forward elimination
    for j=1:r
        x = L(j, :) * unknown_z_vars;
        unknown_z_vars(j, 1) = (b(j) - x) / L(j, j);
    end

    unknown_x_vars = zeros(r, 1);

    % Backward elimination
    for k=r:-1:1
        x = A(k, :) * unknown_x_vars;
        unknown_x_vars(k, 1) = (unknown_z_vars(k) - x) / A(k, k);
    end
    invMat(:, i) = unknown_x_vars;
end
end
