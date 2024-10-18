

function soln = newtons_method(x0, fn, d_fn, opts)
arguments
    x0 {mustBeNumeric}
    fn {mustBeA(fn, "function_handle")}
    d_fn {mustBeA(d_fn, "function_handle")}
    opts.TOL {mustBeFloat} = 1e-6
    opts.MAX_ITER {mustBeInteger} = 1000
end

old_x = x0;

idx = 1;
while idx < opts.MAX_ITER

new_x = old_x - fn(old_x) / d_fn(old_x);

if abs(old_x - new_x) < opts.TOL
    break
end

old_x = new_x;
idx = idx + 1;

end
soln = new_x;
end
