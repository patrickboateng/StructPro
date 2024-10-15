

function x = newtons_method(x, f, d_f, TOL, MAX_ITER)
arguments
    x {mustBeNumeric}
    f {mustBeA(f, "function_handle")}
    d_f {mustBeA(d_f, "function_handle")}
    TOL {mustBeFloat} = 1e-6
    MAX_ITER {mustBeInteger} = 1000
end

old_x = x;

idx = 1;

while idx < MAX_ITER

new_x = old_x - f(old_x) / d_f(old_x);

if abs(old_x - new_x) < TOL
    break
end

old_x = new_x;

idx = idx + 1;
end
    
x = new_x;

end
