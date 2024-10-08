
function X = gauss_jacobi(A, b)

    [r, ~] = size(A);
    tol = 10^-6;
    
    unknown_vars = zeros(r, 1);
    MAX_ITER = 1000000;
    
    iter = 0;
    
    while iter < MAX_ITER
        x_old = unknown_vars;
        for i=1:r
            x = 0;
            for j=1:r
                if i==j
                    continue
                end
                x = x + A(i, j) * x_old(j);  
            end
            unknown_vars(i) = (b(i) - x) / A(i, i);
        end
        % Check the error tolerance
        if norm(unknown_vars - x_old) < tol
            break
        end

        iter = iter + 1;
        
    end

    X = unknown_vars;
    
end
