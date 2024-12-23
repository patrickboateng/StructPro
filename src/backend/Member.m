classdef Member < handle
    properties (Access=protected)
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

        function id = getId(obj)
            id = obj.id;
        end

        function start_node = getStartNode(obj)
            start_node = obj.start_node;
        end

        function end_node = getEndNode(obj)
            end_node = obj.end_node;
        end

        function section = getSection(obj)
            section = obj.section;
        end
    end

    methods (Abstract)

        len(obj)
        stiffness_matrix(obj)

    end
end