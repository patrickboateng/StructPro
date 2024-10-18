function unknown_vars = gauss_jacobi(A, b, opts)
arguments
    A (:, :) double {mustBeMatrix}
    b  double {mustBeColumn}
    opts.TOL {mustBeFloat} = 1e-6
    opts.MAX_ITER {mustBeInteger} = 1000
end

[r, ~] = size(A);

unknown_vars = zeros(r, 1);

idx = 1;

while idx < opts.MAX_ITER
    x_old = unknown_vars;
    for i=1:r
        x = 0;
        for j=1:r
            if i ~= j
                x = x + A(i, j) * x_old(j);
            end
        end
        unknown_vars(i) = (b(i) - x) / A(i, i);
    end
    % Check the error tolerance
    if norm(unknown_vars - x_old) < opts.TOL
        break
    end
    idx = idx + 1;
end 
end
