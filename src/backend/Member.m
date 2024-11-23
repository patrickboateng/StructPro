classdef Member
    properties
        id {mustBeNumeric}
        start_node Node
        end_node Node
        section RectangularSection
        distributed_load UniformDistributedLoad
    end

    methods
        function obj = Member(id, start_node, end_node, section, distributed_load)
            arguments
                id 
                start_node 
                end_node 
                section
                distributed_load
            end
            obj.id = id;
            obj.start_node = start_node;
            obj.end_node = end_node;
            obj.section = section;
            obj.distributed_load = UniformDistributedLoad(distributed_load, 1, 1);
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

        function forces = fixed_end_forces(obj)
            m_len = obj.len();
            w = obj.distributed_load.magnitude;
            forces = [w*m_len / 2 w*m_len / 2];
        end

        function moments = fixed_end_moments(obj)
            m_len = obj.len();
            w = obj.distributed_load.magnitude;
            moments = [(w*m_len^2) / 12 (-1 * w*m_len^2) / 12];
        end
    end
end