classdef PointLoad
    properties
        magnitude (1, 1) {mustBeNumeric}
        node Node
    end

    methods
        function obj = PointLoad(magnitude, node)
            obj.magnitude = magnitude;
            obj.node = node;
        end
    end
end