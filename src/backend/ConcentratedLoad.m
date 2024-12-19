classdef ConcentratedLoad
    properties
        magnitude (1, 1) {mustBeNumeric}
        position Point2D
    end

    methods
        function obj = ConcentratedLoad(magnitude, node)
            arguments
                magnitude (1, 1) {mustBeNumeric}
                node (1, 1)
            end
            obj.magnitude = magnitude;
            obj.position = node.position;
        end

        function r = double(obj)
            r = obj.magnitude;
        end
    end
end