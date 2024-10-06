
function X = bisection_method(a, b, f)

    avg = (a + b) / 2;
    
    f_a = f(a);
    f_b = f(b);
    f_avg = f(avg);
    
    TOL = 1e-6;
    
    i = 1;
    MAX_ITER = 100;
    
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
            
        i = i + 1;
    
        if i > MAX_ITER
            break
        end
        
    end

    X = avg;

end


% disp(avg);
% disp(i);
% 


