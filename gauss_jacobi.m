
function X = gauss_jacobi(A, b, MAX_ITER, TOL)

    if nargin < 3
        MAX_ITER = 1000000;
        TOL = 1e-6;
    elseif nargin < 4
        TOL = 1e-6;
    end

    [r, ~] = size(A);
    
    unknown_vars = zeros(r, 1);
    
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
        if norm(unknown_vars - x_old) < TOL
            break
        end

        iter = iter + 1;
        
    end

    X = unknown_vars;
    
end
