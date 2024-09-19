clc;clearvars

A = [3, -0.1, -0.2; 0.1, 7, -0.3; 0.3, -0.2, 10.0];
b = [7.85; -19.3; 71.4];

A = [4 1 -1; 5 1 2; 6 1 1];
b = [-2; 4; 6];

A = [1 -1 2; -1 5 4; 2 4 29];
b = [2; 6; -3];

A = [45 2 3; -3 22 2; 5 1 20];
b = [58; 47; 67];

%A = [2 4 -2 2 4; 0 1 1 4 6; 0 3 15 2 8; 2 3 5 4 4; 1 1 1 1 5];
%b = [2; 4; 36; 8; 6];

% A = [0 1 1; 2 4 -2; 0 3 15];
% b = [4; 2; 36];

% r will serve as the total number of iterations.
[r, c] = size(A);

if r ~= c, error("Gauss elimination works for square matrices only.")
end

% Augmented matrix
augMat = [A b];

% Forward Elimination
for i=1:r
    % Swap Algorithm
    if augMat(i, i) == 0
        % Swap if pivot == 0
        for k=i+1:r
            if augMat(k, i) ~= 0
                tmp = augMat(i, :);
                augMat(i,:) = augMat(k, :);
                augMat(k, :) = tmp;
                break;
            end
        end

    end
    % Swap end

    if augMat(i, i) == 0, error("")
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
