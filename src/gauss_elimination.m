function unknown_x_vars = gauss_elimination(A, b, opts)
arguments
    A (:, :) double {mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.tol {mustBeFloat} = 1e-6
end

% r will serve as the total number of iterations.
[r, ~] = size(A);

% Augmented matrix assigned to A for code optimization.
A = [A b];

% Forward Elimination
for i=1:r
    % find pivot and swap if zero or close to zero.
    [~, A] = swapRow(A, [], pv_idx=i, total_rows=r, tol=opts.tol);

    for j=i+1:r
        tr_vec = A(i, :) .* (A(j, i) / A(i, i));
        A(j, :) = A(j, :) - tr_vec;
    end
end

unknown_x_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = A(i, 1:r) * unknown_x_vars;
    unknown_x_vars(i, 1) = (A(i, end) - x)/ A(i, i);
end
end
