% Calculating the inverse of a matrix using LU decomposition

% A = [3, -0.1, -0.2; 0.1, 7, -0.3; 0.3, -0.2, 10];

function X = mat_inv(A)
arguments
    A (:, :) {mustBeMatrix}
end
% r will serve as the total number of iterations.
[r, ~] = size(A);

% Lower triangular matrix
L = eye(r);
% Upper triangular matrix
U = A;

TOL = 1e-6;

% Forward Elimination
for i=1:r
% find pivot and swap
max_ = i;
for m =i+1:r
    if abs(U(max_, max_)) > TOL
        break;
    end

    if abs(U(m, i)) > abs(U(i, i))
        max_ = m;
    end
end

if max_ ~= i
    tmp = U(i, :);
    U(i, :) = U(max_, :);
    U(max_, :) = tmp;
end

if abs(U(i, i)) < TOL, error("Singular Matrix")
end 

for j=i+1:r
    factor = (U(j, i) / U(i, i));
    tr_vec = U(i, :) .* factor;
    U(j, :) = U(j, :) - tr_vec;
    L(j, i) = factor;
end
end

I = eye(r);

invMat = zeros(r);

for i=1:r

b = I(:, i);
unknown_z_vars = zeros(r, 1);

% Forward elimination
for j=1:r
    x = L(j, :) * unknown_z_vars;
    x = (b(j) - x) / L(j, j);
    unknown_z_vars(j, 1) = x;
end

unknown_x_vars = zeros(r, 1);

% Backward elimination
for k=r:-1:1
    x = U(k, :) * unknown_x_vars;
    x = (unknown_z_vars(k) - x) / U(k, k);
    unknown_x_vars(k, 1) = x;
end

invMat(:, i) = unknown_x_vars;

end

X = invMat;

end
