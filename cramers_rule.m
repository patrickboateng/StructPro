
function x = cramers_rule(A, b)
arguments
    A (:, :) double {mustBeMatrix}
    b (:, 1) double {mustBeColumn}
end

[r, ~] = size(A);

detA = det(A);

x = zeros(r, 1);

for i=1:r
    tmp = A(:, i);
    A(:, i) = b;
    x(i) = det(A) / detA;
    A(:, i) = tmp;
end
end
