function mustBeSquareMatrix(value)
mustBeMatrix(value);
[r, c] = size(value);
assert(isequal(r, c), "Value must be a square matrix")
end