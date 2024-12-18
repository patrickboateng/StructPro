classdef Member < handle
    properties
        id {mustBePositive, mustBeInteger}
        start_node BmNode
        end_node BmNode
        section Section
    end

    methods
        function obj = Member(id, start_node, end_node, section)
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
    end

    methods (Abstract)

        len(obj)
        stiffness_matrix(obj)

    end
end