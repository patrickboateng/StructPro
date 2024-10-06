
function X = cramers_rule(A, b)

    [r, c] = size(A);
    
    D = det(A);
    
    unkwown_vars = zeros(r, 1);
    
    for i=1:c
        tmp = A(:, i);
        A(:, i) = b;
        unkwown_vars(i) = det(A) / D;
        A(:, i) = tmp;
    end
    X = unkwown_vars;
end
