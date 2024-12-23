classdef Point2D < handle
    properties (GetAccess=public, SetAccess=private)
        x {mustBeNumeric}
        y {mustBeNumeric}
    end

    methods
        function obj = Point2D(x, y)
            obj.x = x;
            obj.y = y;
        end

        function r = eq(obj, other)
            r = obj.x == other.x && obj.y == other.y;
        end

        function setX(obj, val)
            obj.x = val;
        end

        function setY(obj, val)
            obj.y = val;
        end

    end
end