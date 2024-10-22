function A = swapRow(A, opts)
arguments
    A 
    opts.pv_idx
    opts.total_rows
    opts.tol
end

max_ = opts.pv_idx;

% Select pivot
for m =opts.pv_idx+1:opts.total_rows
    if abs(A(max_, max_)) > opts.tol
        break;
    end

    if abs(A(m, opts.pv_idx)) > abs(A(opts.pv_idx, opts.pv_idx))
        max_ = m;
    end
end

% Swap
if max_ ~= opts.pv_idx
    tmp = A(opts.pv_idx, :);
    A(opts.pv_idx, :) = A(max_, :);
    A(max_, :) = tmp;
end

if abs(A(opts.pv_idx, opts.pv_idx)) < opts.tol, error("Singular Matrix")
end 
end