function unknown_x_vars = gauss_jordan(A, b, opts)
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
    A = swapRow(A, pv_idx=i, total_rows=r, tol=opts.tol);

    for j=i+1:r
        A(i, :) = A(i, :) ./ A(i, i);
        A(j, :) = A(j, :) - A(i, :) .* A(j, i);
    end
    A(i, :) = A(i, :) ./ A(i, i);
end

% Backward Elimination
for i=r:-1:1
    for j=i-1:-1:1
        A(j, :) = A(j, :) - A(i, :) .* A(j, i);
    end
end
unknown_x_vars = A(:, end);
end
