clc;clearvars;

A = [1 -1 2; -1 5 4; 2 4 29];
b = [2; 6; -3];

[r, c] = size(A);

D = det(A);

unkwown_vars = zeros(r, 1);

for i=1:c
    tmp = A(:, i);
    A(:, i) = b;
    unkwown_vars(i) = det(A) / D;
    A(:, i) = tmp;
end

disp(unkwown_vars)
