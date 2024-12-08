classdef BmMember
    properties
        id {mustBeNumeric}
        start_node BmNode
        end_node BmNode
        section RectangularSection
        distributed_load UniformDistributedLoad
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

        function m_stiffness = stiffness_matrix(obj)
            m_len = obj.len();
            E = obj.section.E;
            I = obj.section.I;

            k = (E * I) / m_len^3;

            m_stiffness = [12 6*m_len -12 6*m_len; ...
                6*m_len 4*m_len^2 -6*m_len 2*m_len^2; ...
                -12 -6*m_len 12 -6*m_len; ...
                6*m_len 2*m_len^2 -6*m_len 4*m_len^2];

            m_stiffness = m_stiffness .* k;
        end
    end
end