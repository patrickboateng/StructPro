
function x = cramers_rule(A, b)

    [r, c] = size(A);
    
    detA = det(A);
    
    x = zeros(r, 1);
    
    for i=1:c
        tmp = A(:, i);
        A(:, i) = b;
        x(i) = det(A) / detA;
        A(:, i) = tmp;
    end

end
