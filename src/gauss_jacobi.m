function unknown_x_vars = gauss_jacobi(A, b, opts)
arguments
    A (:, :) double {mustBeSquareMatrix}
    b  double {mustBeColumn}
    opts.tol {mustBeFloat} = 1e-6
    opts.max_iter {mustBeInteger} = 1000
end

[r, ~] = size(A);
unknown_x_vars = zeros(r, 1);
old_error = 100;

idx = 1;
while idx < opts.max_iter
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
    
    new_error = solnError(unknown_x_vars, x_old);
    
    if new_error < opts.tol
        break
    end
    
    checkError(new_error, old_error);

    old_error = new_error;
    idx = idx + 1;
end 
end
