function unknown_x_vars = lu_decomposition(A, b, opts)
arguments
    A (:, :) double {mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.tol {mustBeFloat} = 1e-6
end

% r will serve as the total number of iterations.
[r, ~] = size(A);

% Lower triangular matrix
L = eye(r);

% Forward Elimination
for i=1:r
    % find pivot and swap if zero or close to zero.
    A = swap(A, pv_idx=i, total_rows=r, tol=opts.tol);

    for j=i+1:r
        factor = (A(j, i) / A(i, i));
        A(j, :) = A(j, :) - A(i, :) .* factor;
        L(j, i) = factor;
    end
end

unknown_z_vars = zeros(r, 1);

% Forward Substitution
for i=1:r
    x = L(i, :) * unknown_z_vars;
    unknown_z_vars(i, 1) = (b(i) - x)/ L(i, i);
end

unknown_x_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = A(i, :) * unknown_x_vars;
    unknown_x_vars(i, 1) = (unknown_z_vars(i) - x)/ A(i, i);
end
end
