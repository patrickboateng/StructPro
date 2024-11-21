function vars_i = modified_newtons_diff_solver(funcs, vars, vars_i, opts)
arguments
    funcs (1, :) {mustBeRow}
    vars (1, :)  {mustBeRow}
    vars_i (1, :) double {mustBeRow}
    opts.MaxIter = 1000
end

[~, c] = size(vars);
A = size(c);
b = zeros(c, 1);
iter = 1;

while iter < opts.MaxIter
    for i=1:c
        for j=1:c
            A(i, j) = subs(diff(funcs(i), vars(j)), vars_i(j));
        end
        b(i) = -1 * subs(funcs(i), vars, vars_i);
    end

    soln = A \ b;
    
    if sum(abs(soln)) < 1e-4
        break;
    end
    vars_i = vars_i + soln';
    iter = iter + 1;
end
end
