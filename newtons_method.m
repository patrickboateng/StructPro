

function X = newtons_method(X, f, d_f, TOL, MAX_ITER)

if nargin < 4
    TOL = 1e-6;
    MAX_ITER = 1000;
end

if nargin < 5
    MAX_ITER = 1000;
end

old_x = X;

idx = 1;

while idx < MAX_ITER

    new_x = old_x - f(old_x) / d_f(old_x);
    
    if abs(old_x - new_x) < TOL
        break
    end

    old_x = new_x;

    idx = idx + 1;
end
    
X = new_x;

end
