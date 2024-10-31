function avg = bisection_method(fn, a, b, opts)
arguments
    fn {mustBeA(fn, "function_handle")}
    a (1, 1) {mustBeNumeric}
    b (1, 1) {mustBeNumeric}
    opts.Tol (1, 1) {mustBeFloat} = 1e-6
    opts.MaxIter (1, 1) {mustBeInteger} = 10000
end

f_a = fn(a);
f_b = fn(b);

idx = 1;

while idx < opts.MaxIter

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

    if abs(b - a) < opts.Tol
        break
    end     

    idx = idx + 1;
end
avg = (a + b) / 2;
end
