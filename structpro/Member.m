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
    end
end