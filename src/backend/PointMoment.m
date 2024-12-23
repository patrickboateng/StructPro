classdef PointMoment < ConcentratedLoad

    methods
        function obj = plus(obj, other)
            check(obj, other)
            obj.magnitude = double(obj) + double(other);
        end

        function obj = minus(obj, other)
            check(obj, other)
            obj.magnitude = double(obj) - double(other);
        end

        function check(obj, other)
            if ~(isa(other, "PointMoment") && obj.position == other.position)
                error("other must be a PointMoment and have the " + ...
                    "position as obj")
            end
        end
    end
end