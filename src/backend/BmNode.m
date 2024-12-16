classdef BmNode < handle
    properties 
        id {mustBeInteger}
        position Point2D
        support  Support2D
        point_load PointLoad
        point_moment PointMoment
        fixed_end_force PointLoad
        fixed_end_moment PointMoment
        reaction_force PointLoad
        reaction_moment PointMoment
    end

    methods
        function obj = BmNode(id, x, y, ...
                            point_load, ...
                            point_moment, rx, ry, rm)
            arguments
                id {mustBeInteger}
                x {mustBeNumeric}
                y {mustBeNumeric}
                point_load double
                point_moment double
                rx {mustBeNumericOrLogical} = 0
                ry {mustBeNumericOrLogical} = 0
                rm {mustBeNumericOrLogical} = 0                
            end
            obj.id = id;
            obj.position = Point2D(x, y);
            obj.support = Support2D(rx, ry, rm);

            obj.point_load = PointLoad(point_load, obj);
            obj.point_moment = PointMoment(point_moment, obj);
            obj.fixed_end_force = PointLoad(0, obj);
            obj.fixed_end_moment = PointMoment(0, obj);

            obj.reaction_force = PointLoad(0, obj);
            obj.reaction_moment = PointMoment(0, obj);
        end
    end
end