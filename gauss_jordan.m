
function x = gauss_jordan(A, b, TOL)
arguments
    A (:, :) double {mustBeMatrix, mustBeSquareMatrix}
    b  double {mustBeColumn}
    TOL {mustBeFloat} = 1e-6
end

% r will serve as the total number of iterations.
[r, ~] = size(A);

% Augmented matrix
augMat = [A b];

% Forward Elimination
for i=1:r
max_ = i;
for m =i+1:r
    if abs(augMat(max_, max_)) > TOL
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

if abs(augMat(i, i)) < TOL, error("Singular Matrix")
end 

for j=i+1:r
augMat(i, :) = augMat(i, :) ./ augMat(i, i);
tr_vec = augMat(i, :) .* augMat(j, i);
augMat(j, :) = augMat(j, :) - tr_vec;
end

augMat(i, :) = augMat(i, :) ./ augMat(i, i);

end

% Backward Elimination
for i=r:-1:1
   for j=i-1:-1:1
   tr_vec = augMat(i, :) .* augMat(j, i);
   augMat(j, :) = augMat(j, :) - tr_vec;
   end
end
x = augMat(:, end);
end

function mustBeSquareMatrix(A)
[r, c] = size(A);
assert(isequal(r, c), "Value must be a square matrix")
end
