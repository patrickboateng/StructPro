classdef PointLoad < ConcentratedLoad
    properties
        direction LoadDirection
    end

    methods
        function obj = PointLoad(magnitude, node, direction)
            arguments
                magnitude (1, 1) {mustBeNumeric}
                node (1, 1) Node
                direction (1, 1) LoadDirection = LoadDirection.VERTICAL
            end
            obj@ConcentratedLoad(magnitude, node);
            obj.direction = direction;
        end

        function obj = plus(obj, other)
            check(obj, other);
            obj.magnitude = double(obj) + double(other);
        end

        function obj = minus(obj, other)
            check(obj, other);
            obj.magnitude = double(obj) - double(other);
        end

        function check(obj, other)
            if ~(isa(obj, "PointLoad") && isa(other, "PointLoad") ...
                    && (obj.position == other.position) ...
                    && (obj.direction == other.direction))
                msg = ("other must be a PointLoad and have the " + ...
                    "same position and direction as obj");
                error(msg);
            end
        end

    end
end