
function unknown_x_vars = lu_decomposition(A, b, opts)
arguments
    A (:, :) double {mustBeMatrix, mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.TOL {mustBeFloat} = 1e-6
end

% r will serve as the total number of iterations.
[r, ~] = size(A);

% Lower triangular matrix
L = eye(r);

% Upper triangular matrix
U = A;

% Forward Elimination
for i=1:r
    % find pivot and swap
    max_ = i;
    for m =i+1:r
        if abs(U(max_, max_)) > opts.TOL
            break;
        end

        if abs(U(m, i)) > abs(U(i, i))
            max_ = m;
        end
    end

    if max_ ~= i
        tmp = U(i, :);
        U(i, :) = U(max_, :);
        U(max_, :) = tmp;
    end

    if abs(U(i, i)) < opts.TOL, error("Singular Matrix")
    end

    for j=i+1:r
        factor = (U(j, i) / U(i, i));
        U(j, :) = U(j, :) - U(i, :) .* factor;
        L(j, i) = factor;
    end
end

unknown_z_vars = zeros(r, 1);

% Forward Substitution
for i=1:r
    x = L(i, :) * unknown_z_vars;
    x = (b(i) - x)/ L(i, i);
    unknown_z_vars(i, 1) = x;
end

z = unknown_z_vars;

unknown_x_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = U(i, :) * unknown_x_vars;
    unknown_x_vars(i, 1) = (z(i) - x)/ U(i, i);
end
end

function mustBeSquareMatrix(A)
[r, c] = size(A);
assert(isequal(r, c), "Value must be a square matrix")
end
