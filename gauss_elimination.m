function unknown_x_vars = gauss_elimination(A, b, opts)
arguments
    A (:, :) double {mustBeMatrix, mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.TOL {mustBeFloat} = 1e-6
end

% r will serve as the total number of iterations.
[r, ~] = size(A);

% Augmented matrix assigned to A for code optimization.
A = [A b]; 

% Forward Elimination
for i=1:r
    % find pivot and swap if zero or close to zero.
    A = swap(A, pv_idx=1, total_rows=r, TOL=opts.TOL);

    for j=i+1:r
        tr_vec = A(i, :) .* (A(j, i) / A(i, i));
        A(j, :) = A(j, :) - tr_vec;
    end
end

unknown_x_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = A(i, 1:r) * unknown_x_vars;
    x = (A(i, end) - x)/ A(i, i);
    unknown_x_vars(i, 1) = x;
end
end
