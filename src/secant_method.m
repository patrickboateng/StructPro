function soln = secant_method(fn, x_0, x_1, opts)
arguments
    fn {mustBeA(fn, "function_handle")}
    x_0 {mustBeNumeric}
    x_1 {mustBeNumeric}
    opts.Tol {mustBeFloat} = 1e-6
    opts.MaxIter {mustBeInteger} = 1000
end

idx = 1;
while idx < opts.MaxIter
    g_x1 = (fn(x_1) - fn(x_0)) / (x_1 - x_0);
    x2 = x_1  - fn(x_1) / g_x1;

    x_0 = x_1;
    x_1 = x2;

    if abs(x_1 - x_0) < opts.Tol
        break
    end

    idx = idx + 1;
end
soln = x_1;
end
