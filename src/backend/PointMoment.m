classdef PointMoment
    
    properties
        magnitude (1, 1) {mustBeNumeric}
        position Point2D
    end

    methods
        function obj = PointMoment(magnitude, node)
            arguments
                magnitude (1, 1) {mustBeNumeric}
                node (1, 1) 
            end
            obj.magnitude = magnitude;
            obj.position = node.position;
        end
    end


end