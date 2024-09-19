clc;clearvars

A = [4 1 -1; 2 7 1; 1 -3 12];
b = [3; 19; 31];
% A = [1 -1; 2 -3];
% b = [10; -6];

[r, ~] = size(A);
tol = 10^-6;

unknown_vars = zeros(r, 1);

while true
    x_old = unknown_vars;
    for i=1:r
        x = 0;
        for j=1:r
            if i==j
                continue
            end
            x = x + A(i, j) * unknown_vars(j);
            unknown_vars(i) = (b(i) - x) / A(i, i);
        end
    end
    if norm(unknown_vars - x_old) < tol
        break
    end
end

unknown_vars
