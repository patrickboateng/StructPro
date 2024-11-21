function [P, A] = swapRow(A, P, opts)
arguments
    A
    P
    opts.PvIdx
    opts.TotalRows
    opts.Tol
end

if ~(isempty(P))
    mustBeMatrix(P);
end

max_idx = opts.PvIdx;

% Select pivot
for m =opts.PvIdx+1:opts.TotalRows
    if abs(A(max_idx, max_idx)) > opts.Tol
        break
    end
    if abs(A(m, opts.PvIdx)) > abs(A(opts.PvIdx, opts.PvIdx))
        max_idx = m;
    end
end

% Swap
if max_idx ~= opts.PvIdx
    A = swap(A, opts.PvIdx, max_idx);
    if ~isempty(P)
        P = swap(P, opts.PvIdx, max_idx);
    end
end

if abs(A(opts.PvIdx, opts.PvIdx)) < opts.Tol
    error("Singular Matrix")
end
end

function A = swap(A, idx1, idx2)
tmp = A(idx1, :);
A(idx1, :) = A(idx2, :);
A(idx2, :) = tmp;
end
