function mustBeSquareMatrix(A)
[r, c] = size(A);
assert(isequal(r, c), "Value must be a square matrix")
end