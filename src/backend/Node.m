classdef Node < handle
    properties (Access=protected)
        id {mustBeInteger}
        position Point2D
        support  Support2D
        point_load PointLoad
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

            obj.displacement = 0;
            obj.rotation = 0;
        end

        function id = getId(obj)
            id = obj.id;
        end

        function position = getPosition(obj)
            position = obj.position;
        end

        function support = getSupport(obj)
            support = obj.support;
        end

        function point_load = getPointLoad(obj)
            point_load = obj.point_load;
        end

        function point_moment = getPointMoment(obj)
            point_moment = obj.point_moment;
        end

        function fixed_end_force = getFixedEndForce(obj)
            fixed_end_force = obj.fixed_end_force;
        end

        function setFixedEndForce(obj, val)
            obj.fixed_end_force = val;
        end

        function fixed_end_moment = getFixedEndMoment(obj)
            fixed_end_moment = obj.fixed_end_moment;
        end

        function setFixedEndMoment(obj, val)
            obj.fixed_end_moment = val;
        end

        function reaction_force = getReactionForce(obj)
            reaction_force = obj.reaction_force;
        end

        function setReactionForce(obj, val)
            obj.reaction_force = val;
        end

        function reaction_moment = getReactionMoment(obj)
            reaction_moment = obj.reaction_moment;
        end

        function setReactionMoment(obj, val)
            obj.reaction_moment = val;
        end

        function displacement = getDisplacement(obj)
            displacement = obj.displacement;
        end

        function setDisplacement(obj, val)
            obj.displacement = val;
        end

        function rotation = getRotation(obj)
            rotation = obj.rotation;
        end

        function setRotation(obj, val)
            obj.rotation = val;
        end
    end
end