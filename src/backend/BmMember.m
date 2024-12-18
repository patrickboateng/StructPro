classdef BmMember < Member
    methods
        function len = len(obj)
            len = obj.end_node.position.x - obj.start_node.position.x;
        end

        function k_local = stiffness_matrix(obj)
            L = obj.len();
            E = obj.section.E;
            I = obj.section.I;

            k = (E * I) / L^3;

            k_local = [12    6*L    -12    6*L; ...
                       6*L   4*L^2  -6*L   2*L^2; ...
                       -12   -6*L     12   -6*L; ...
                       6*L   2*L^2  -6*L   4*L^2];

            k_local = k_local .* k;
        end
    end
end