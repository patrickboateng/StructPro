classdef ConcentratedLoad
    properties (Access=protected)
        magnitude (1, 1) {mustBeNumeric}
        position Point2D
    end

    methods
        function obj = ConcentratedLoad(magnitude, node)
            arguments
                magnitude (1, 1) {mustBeNumeric}
                node (1, 1) Node
            end
            obj.magnitude = magnitude;
            obj.position = node.getPosition();
        end

        function magnitude = getMagnitude(obj)
            magnitude = double(obj);
        end

        function position = getPosition(obj)
            position = obj.position;
        end

        function r = double(obj)
            r = obj.magnitude;
        end
    end
end
