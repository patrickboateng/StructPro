classdef FrMember < Member
    methods
        function len = len(obj)
            start_pos = obj.start_node.position;
            end_pos = obj.end_node.position;
            len = sqrt((end_pos.x - start_pos.x)^2 + ...
                       (end_pos.y - start_pos.y)^2);
        end

        function k_global_mat = stiffness_matrix(obj)
            L = obj.len();
            E = obj.section.E;
            I = obj.section.I;
            A = obj.section.A;
            
            k = (E * I) / L^3;
                        
            k_local_mat = ...
            [ (A*L^2)/I     0      0  (-1*A*L^2)/I     0      0; ...
                      0    12    6*L             0   -12    6*L; ...
                      0   6*L  4*L^2             0  -6*L  2*L^2; ...
           (-1*A*L^2)/I     0      0     (A*L^2)/I     0      0; ...
                      0   -12   -6*L             0    12   -6*L; ...
                      0   6*L  2*L^2             0  -6*L   4*L^2;...
                ];
            
            start_pos = obj.start_node.position;
            end_pos = obj.end_node.position;

            ld_x = (end_pos.x - start_pos.x) / L;
            ld_y = (end_pos.y - start_pos.y) / L;

            T = [ ld_x ld_y 0     0    0  0;
                 -ld_y ld_x 0     0    0  0;
                     0    0 1     0    0  0;
                     0    0 0  ld_x ld_y  0;
                     0    0 0 -ld_y ld_x  0;
                     0    0 0     0    0  1];

            k_local_mat = k_local_mat .* k;
            k_global_mat = T' * k_local_mat * T;
        end
    end
end