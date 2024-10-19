function unknown_x_vars = gauss_jacobi(A, b, opts)
arguments
    A (:, :) double {mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.TOL {mustBeFloat} = 1e-6
    opts.MAX_ITER {mustBeInteger} = 1000
end

[r, ~] = size(A);

unknown_x_vars = zeros(r, 1);

idx = 1;

while idx < opts.MAX_ITER
    x_old = unknown_x_vars;
    for i=1:r
        x = 0;
        for j=1:r
            if i ~= j
                x = x + A(i, j) * x_old(j);
            end
        end
        unknown_x_vars(i) = (b(i) - x) / A(i, i);
    end
    
    new_error = norm(unknown_x_vars - x_old);
    
    if new_error < opts.TOL
        break
    end
    
    if idx > 1
        if ~(new_error - old_error < 0)
            warning("Solution is not converging.")
        end
    end
    old_error = new_error;
    idx = idx + 1;
end 
end
