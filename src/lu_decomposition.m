function unknown_x_vars = lu_decomposition(A, b, opts)
arguments
    A (:, :) double {mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.Tol {mustBeFloat} = 1e-6
end
[r, ~] = size(A);
[P, L, U] = lu_factor(A, tol=opts.Tol);
b = P * b;

unknown_z_vars = zeros(r, 1);

% Forward Substitution
for i=1:r
    x = L(i, :) * unknown_z_vars;
    unknown_z_vars(i, 1) = (b(i) - x) / L(i, i);
end

unknown_x_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = U(i, :) * unknown_x_vars;
    unknown_x_vars(i, 1) = (unknown_z_vars(i) - x) / U(i, i);
end
end
