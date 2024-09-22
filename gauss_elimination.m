clc;clearvars

A = [4 1 -1; 5 1 2; 6 1 1];
b = [-2; 4; 6];

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
    x = augMat(i, 1:r) * unknown_vars;
    x = (augMat(i, end) - x)/ augMat(i, i);
    unknown_vars(i, 1) = x;
end

disp(unknown_vars)