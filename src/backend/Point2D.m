classdef Point2D
    properties
        x {mustBeNumeric}
        y {mustBeNumeric}
    end

    methods
        function obj = Point2D(x, y)
            obj.x = x;
            obj.y = y;
        end
    end
end