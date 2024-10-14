
function X = bisection_method(a, b, f, MAX_ITER)

    if nargin < 4
        MAX_ITER = 100;
    end
    avg = (a + b) / 2;
    
    f_a = f(a);
    f_b = f(b);
    f_avg = f(avg);
    
    TOL = 1e-6;
    
    idx = 1;
    
    while f_a * f_b < 0
        
        if f_avg < 0 && f_a < 0 || f_avg > 0 && f_a > 0
            a = avg;
        end
    
        if f_avg < 0 && f_b < 0 || f_avg > 0 && f_b > 0
            b = avg;
        end
    
        avg = (a + b) / 2;
    
        f_avg = f(avg);
    
        if abs(b - a) < TOL
            break
        end
            
        idx = idx + 1;
    
        if idx > MAX_ITER
            break
        end
        
    end
    X = avg;
end
