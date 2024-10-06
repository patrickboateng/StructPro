
function X = gauss_seidel(A, b)

    [r, ~] = size(A);
    tol = 1e-6;
    
    unknown_vars = zeros(r, 1);
    
    % global_errors = zeros(1, r);
    
    % iter = 1;
    
    MAX_ITER = 1000000;
    iter = 0;
    
    while iter < MAX_ITER
        x_old = unknown_vars;
        for i=1:r
            x = 0;
            for j=1:r
                if i==j
                    continue
                end
                x = x + A(i, j) * unknown_vars(j);
            end
            unknown_vars(i) = (b(i) - x) / A(i, i);
        end
        
        % Calculate error for each variable
        % local_errors = zeros(1, r);
        % for k=1:r
        %     err = ((unknown_vars(k) - x_old(k)) / unknown_vars(k)) * 100;
        %     local_errors(k) = abs(err);
        % end
        % 
        % global_errors(iter, :) = local_errors;
        % 
        % iter = iter + 1;
    
        % Check the error tolerance
        % if max(local_errors) < tol
        %     break
        % end
        if norm(unknown_vars - x_old) < tol
            break
        end
        iter = iter + 1;
    
    end
        X = unknown_vars;
end
% disp(global_errors);
% disp(unknown_vars);

% number_of_iterations = 1:length(global_errors);
% 
% for it=1:r
%     plot(number_of_iterations, global_errors(:, it))
%     hold on
% end
% legend
% title("A graph of Errors against No. of iterations")

% help plot