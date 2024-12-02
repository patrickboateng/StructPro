classdef Node < handle
    properties 
        id {mustBeInteger}
        position Point2D
        support  Support2D
        ver_point_load PointLoad
        lat_point_load PointLoad
        point_moment PointMoment
        fixed_end_force PointLoad
        fixed_end_moment PointMoment
        reaction_force PointLoad
        reaction_moment PointMoment
        displacement double
        rotation double
    end

    methods
        function obj = Node(id, x, y, ...
                            lat_point_load, ver_point_load, ...
                            point_moment, rx, ry, rm)
            arguments
                id {mustBeInteger}
                x {mustBeNumeric}
                y {mustBeNumeric}
                lat_point_load double
                ver_point_load double
                point_moment double
                rx {mustBeNumericOrLogical} = 0
                ry {mustBeNumericOrLogical} = 0
                rm {mustBeNumericOrLogical} = 0                
            end
            obj.id = id;
            obj.position = Point2D(x, y);
            obj.support = Support2D(rx, ry, rm);
            obj.lat_point_load = PointLoad(lat_point_load, obj);
            obj.ver_point_load = PointLoad(ver_point_load, obj);
            obj.point_moment = PointMoment(point_moment, obj);
            obj.fixed_end_force = PointLoad(0, obj);
            obj.fixed_end_moment = PointMoment(0, obj);
            obj.reaction_force = PointLoad(0, obj);
            obj.reaction_moment = PointMoment(0, obj);
            obj.displacement = 0;
            obj.rotation = 0;
        end

    end
end