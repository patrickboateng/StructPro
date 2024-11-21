function [largest_eig_val, norm_eig_vec] = power_method(A, opts)
arguments
    A 
    opts.MaxIter (1, 1) = 1000
end

[r, ~] = size(A);

norm_eig_vec = rand(r, 1);
prev_largest_eig_val = max(abs(norm_eig_vec));

iter = 1;
while iter < opts.MaxIter
    eig_vec = A * norm_eig_vec;
    largest_eig_val = max(abs(eig_vec));
    norm_eig_vec = eig_vec ./ largest_eig_val;
    
    if abs(largest_eig_val - prev_largest_eig_val) < 1e-6
        break
    end

    prev_largest_eig_val = largest_eig_val;

    iter = iter + 1;
   
end

end
