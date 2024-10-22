function [L, U] = lu_factor(A, opts)
arguments
    A double {mustBeMatrix}
    opts.tol {mustBeFloat} = 1e-6
end
% r will serve as the total number of iterations.
[r, ~] = size(A);

% Lower triangular matrix
L = eye(r);

% Forward Elimination
for i=1:r
    % find pivot and swap if zero or close to zero.
    A = swapRow(A, pv_idx=i, total_rows=r, tol=opts.tol);

    for j=i+1:r
        factor = (A(j, i) / A(i, i));
        A(j, :) = A(j, :) - A(i, :) .* factor;
        L(j, i) = factor;
    end
end
U = A;
end