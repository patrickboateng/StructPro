clc;clearvars

A = [3, -0.1, -0.2; 0.1, 7, -0.3; 0.3, -0.2, 10.0];
b = [7.85; -19.3; 71.4];

A = [4 1 -1; 5 1 2; 6 1 1];
b = [-2; 4; 6];

A = [45 2 3; -3 22 2; 5 1 20];
b = [58; 47; 67];

A = [1 -1; 2 -3];
b = [10; -6];

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
    for j=i+1:r
        tr_vec = augMat(i, :) .* (augMat(j, i) / augMat(i, i));
        augMat(j, :) = augMat(j, :) - tr_vec;
    end
end

unknown_vars = zeros(r, 1);

% Backward Substitution
for i=r:-1:1
    x = 0;
    for j=r:-1:1
        x = x + augMat(i, j) * unknown_vars(j, 1);
    end
    x = (augMat(i, end) - x)/ augMat(i, i);
    unknown_vars(i, 1) = x;
end

disp(unknown_vars)