
function unknown_x_vars = cramers_rule(A, b)
arguments
    A (:, :) double {mustBeSquareMatrix}
    b (:, 1) double {mustBeColumn}
end

[r, ~] = size(A);

detM = det(A);

unknown_x_vars = zeros(r, 1);

for i=1:r
    tmp = A(:, i);
    A(:, i) = b;
    unknown_x_vars(i) = det(A) / detM;
    A(:, i) = tmp;
end
end
