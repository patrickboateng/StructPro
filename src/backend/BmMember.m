classdef BmMember
    properties
        id {mustBePositive, mustBeInteger}
        start_node BmNode
        end_node BmNode
        section RectangularSection
    end

    methods
        function obj = BmMember(id, start_node, end_node, section)
            arguments
                id
                start_node
                end_node
                section
            end
            obj.id = id;
            obj.start_node = start_node;
            obj.end_node = end_node;
            obj.section = section;
        end

        function len = len(obj)
            len = obj.end_node.position.x - obj.start_node.position.x;
        end

        function k_local = stiffness_matrix(obj)
            L = obj.len();
            E = obj.section.E;
            I = obj.section.I;

            k = (E * I) / L^3;

            k_local = [12   6*L    -12    6*L; ...
                       6*L  4*L^2  -6*L   2*L^2; ...
                       -12  -6*L     12   -6*L; ...
                       6*L  2*L^2  -6*L   4*L^2];

            k_local = k_local .* k;
        end
    end
end