
function X = gauss_elimination(A, b)

    % r will serve as the total number of iterations.
    [r, c] = size(A);
    
    if r ~= c, error("Gauss elimination works for square matrices only.")
    end
    
    % Augmented matrix
    augMat = [A b];
    
    TOL = 1e-6;
    
    % Forward Elimination
    for i=1:r
        % find pivot and swap
        max_ = i;
        for m =i+1:r
            if abs(augMat(max_, max_)) > TOL
                break;
            end
    
            if abs(augMat(m, i)) > abs(augMat(i, i))
                max_ = m;
            end
        end
        
        if max_ ~= i
            tmp = augMat(i, :);
            augMat(i, :) = augMat(max_, :);
            augMat(max_, :) = tmp;
        end
    
        if abs(augMat(i, i)) < TOL, error("Singular Matrix")
        end 
    
        for j=i+1:r
            tr_vec = augMat(i, :) .* (augMat(j, i) / augMat(i, i));
            augMat(j, :) = augMat(j, :) - tr_vec;
        end
    end
    
    unknown_vars = zeros(r, 1);
    
    % Backward Substitution
    for i=r:-1:1
        x = augMat(i, 1:r) * unknown_vars;
        x = (augMat(i, end) - x)/ augMat(i, i);
        unknown_vars(i, 1) = x;
    end
    
    X = unknown_vars;
end
