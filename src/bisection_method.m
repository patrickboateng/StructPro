function avg = bisection_method(a, b, fn, opts)
arguments
    a (1, 1) {mustBeNumeric}
    b (1, 1) {mustBeNumeric}
    fn {mustBeA(fn, "function_handle")}
    opts.tol (1, 1) {mustBeFloat} = 1e-6
    opts.max_iter (1, 1) {mustBeInteger} = 10000
end

f_a = fn(a);
f_b = fn(b);

idx = 1;

while idx < opts.max_iter

    avg = (a + b) / 2;
    f_avg = fn(avg);
    
    if ~ (f_a * f_b < 0)
        break
    end
    
    if f_avg < 0 && f_a < 0 || f_avg > 0 && f_a > 0
        a = avg;
    else
        b = avg;
    end

    if abs(b - a) < opts.tol
        break
    end     

    idx = idx + 1;
end
avg = (a + b) / 2;
end
