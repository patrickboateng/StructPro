
function X = lu_decomposition(A, b)

    % r will serve as the total number of iterations.
    [r, c] = size(A);
    
    if r ~= c, error("LU Decomposition works for square matrices only.")
    end
    
    % Lower triangular matrix
    L = eye(r);
    
    % Upper triangular matrix
    U = A;
    
    TOL = 1e-6;
    
    % Forward Elimination
    for i=1:r
        % find pivot and swap
        max_ = i;
        for m =i+1:r
            if abs(U(max_, max_)) > TOL
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
    
        if abs(U(i, i)) < TOL, error("Singular Matrix")
        end
    
        for j=i+1:r
            factor = (U(j, i) / U(i, i));
            tr_vec = U(i, :) .* factor;
            U(j, :) = U(j, :) - tr_vec;
            L(j, i) = factor;
        end
    end
    
    unknown_z_vars = zeros(r, 1);
    
    % Forward Substitution
    for i=1:r
        x = sum(L(i, :)' .* unknown_z_vars);
        x = (b(i) - x)/ L(i, i);
        unknown_z_vars(i, 1) = x;
    end
    
    z = unknown_z_vars;
    
    unknown_x_vars = zeros(r, 1);
    
    % Backward Substitution
    for i=r:-1:1
        x = U(i, :) * unknown_x_vars;
        x = (z(i) - x)/ U(i, i);
        unknown_x_vars(i, 1) = x;
    end
    X = unknown_x_vars;
end

