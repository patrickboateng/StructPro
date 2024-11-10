function [eig_vecs, eig_vals] = modified_power_method(A)

[r, ~] = size(A);
eig_vecs = zeros(r);
eig_vals = zeros(r);

for i=1:r
    [eig_val, eig_vec] = power_method(A);
    norm_eig_vec = eig_vec ./ norm(eig_vec);
    A = A - eig_val * (norm_eig_vec * norm_eig_vec');
    
    idx = r - i + 1;
    eig_vecs(:, idx) = eig_vec;
    eig_vals(idx, idx) = eig_val;
end

end
