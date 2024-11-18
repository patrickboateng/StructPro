classdef Member
    properties
        id {mustBeNumeric}
        start_node Node
        end_node Node
        section RectangularSection
    end

    methods
        function obj = Member(id, node_1, node_2, section)
            obj.id = id;
            obj.start_node = node_1;
            obj.end_node = node_2;
            obj.section = section;
        end

        function len = member_length(obj)
            len = obj.end_node.position.x - obj.start_node.position.x;
        end

        function m_stiffness = member_stiffness_matrix(obj)
            m_len = obj.member_length();
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