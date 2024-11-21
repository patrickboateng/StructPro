classdef PointMoment
    
    properties
        magnitude (1, 1) {mustBeNumeric}
        position Node
    end

    methods
        function obj = PointMoment(magnitude, node)
            obj.magnitude = magnitude;
            obj.position = node;
        end
    end


end