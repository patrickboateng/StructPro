clc;clearvars

A = [3, -0.1, -0.2; 0.1, 7, -0.3; 0.3, -0.2, 10.0];
b = [7.85; -19.3; 71.4];

A = [4 1 -1; 5 1 2; 6 1 1];
b = [-2; 4; 6];

A = [1 -1 2; -1 5 4; 2 4 29];
b = [2; 6; -3];

A = [45 2 3; -3 22 2; 5 1 20];
b = [58; 47; 67];

A = [
    0.5 0 0.866 0 0 0;
    -0.866 0 0.5 0 0 0;
    0.5 0 0 1 0 0;
    0.866 1 0 0 0 1;
    0 0 0.866 0 1 0;
    0 1 0.5 0 0 0;  
];

b = [-1000; 0; 0; 0; 0; 0];

% r will serve as the total number of iterations.
[r, c] = size(A);

if r ~= c, error("Gauss elimination works for square matrices only.")
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

for i=r:-1:1
    for j=i-1:-1:1
       tr_vec = augMat(i, :) .* augMat(j, i);
       augMat(j, :) = augMat(j, :) - tr_vec;
    end
end

augMat
