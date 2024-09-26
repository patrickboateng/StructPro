clc;clearvars

A = [4 1 -1; 2 7 1; 1 -3 12];
b = [3; 19; 31];

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
        end
        unknown_vars(i) = (b(i) - x) / A(i, i);
    end
    % Check the error tolerance
    if norm(unknown_vars - x_old) < tol
        break
    end
end

disp(unknown_vars);
