function soln = newtons_method(fn, diff_fn, x0, opts)
arguments
    fn {mustBeA(fn, "function_handle")}
    diff_fn {mustBeA(diff_fn, "function_handle")}
    x0 {mustBeNumeric}
    opts.Tol {mustBeFloat} = 1e-6
    opts.MaxIter {mustBeInteger} = 1000
end

old_x = x0;
idx = 1;

while idx < opts.MaxIter
    new_x = old_x - fn(old_x) / diff_fn(old_x);

    if abs(old_x - new_x) < opts.Tol
        break
    end
    
    old_x = new_x;
    idx = idx + 1;
end
soln = new_x;
end
