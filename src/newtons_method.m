function soln = newtons_method(x0, fn, diff_fn, opts)
arguments
    x0 {mustBeNumeric}
    fn {mustBeA(fn, "function_handle")}
    diff_fn {mustBeA(diff_fn, "function_handle")}
    opts.tol {mustBeFloat} = 1e-6
    opts.max_iter {mustBeInteger} = 1000
end

old_x = x0;
idx = 1;

while idx < opts.max_iter
    new_x = old_x - fn(old_x) / diff_fn(old_x);

    if abs(old_x - new_x) < opts.tol
        break
    end
    
    old_x = new_x;
    idx = idx + 1;
end
soln = new_x;
end
