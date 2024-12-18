classdef PointLoad < handle
    properties 
        magnitude {mustBeNumeric}
        position Point2D
        direction LoadDirection
    end

    methods
        function obj = PointLoad(magnitude, node, direction)
            arguments
                magnitude (1, 1) {mustBeNumeric}
                node (1, 1) Node
                direction (1, 1) LoadDirection = LoadDirection.VERTICAL
            end
            obj.magnitude = magnitude;
            obj.position = node.position; 
            obj.direction = direction;
        end
    end
end