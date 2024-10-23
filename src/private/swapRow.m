function [P, A] = swapRow(A, P, opts)
arguments
    A
    P
    opts.pv_idx
    opts.total_rows
    opts.tol
end

if ~(isempty(P))
    mustBeMatrix(P);
end

max_idx = opts.pv_idx;

% Select pivot
for m =opts.pv_idx+1:opts.total_rows
    if abs(A(max_idx, max_idx)) > opts.tol
        break
    end
    if abs(A(m, opts.pv_idx)) > abs(A(opts.pv_idx, opts.pv_idx))
        max_idx = m;
    end
end

% Swap
if max_idx ~= opts.pv_idx
    A = swap(A, opts.pv_idx, max_idx);
    if ~isempty(P)
        P = swap(P, opts.pv_idx, max_idx);
    end
end

if abs(A(opts.pv_idx, opts.pv_idx)) < opts.tol
    error("Singular Matrix")
end
end

function A = swap(A, idx1, idx2)
tmp = A(idx1, :);
A(idx1, :) = A(idx2, :);
A(idx2, :) = tmp;
end
