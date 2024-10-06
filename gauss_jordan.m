
function X = gauss_jordan(A, b)

    % r will serve as the total number of iterations.
    [r, c] = size(A);
    
    if r ~= c, error("Gauss Jordan works for square matrices only.")
    end
    
    % Augmented matrix
    augMat = [A b];
    
    EPSILON = 1e-6;
    
    % Forward Elimination
    for i=1:r
    
        max_ = i;
        for m =i+1:r
            if abs(augMat(max_, max_)) > EPSILON
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
    
        if abs(augMat(i, i)) < EPSILON, error("Singular Matrix")
        end 
    
        for j=i+1:r
            augMat(i, :) = augMat(i, :) ./ augMat(i, i);
            tr_vec = augMat(i, :) .* (augMat(j, i) / augMat(i, i));
            augMat(j, :) = augMat(j, :) - tr_vec;
        end
        augMat(i, :) = augMat(i, :) ./ augMat(i, i);
    end

    % Backward Elimination
    for i=r:-1:1
        for j=i-1:-1:1
           tr_vec = augMat(i, :) .* augMat(j, i);
           augMat(j, :) = augMat(j, :) - tr_vec;
        end
    end
    X = augMat(:, end);
end
