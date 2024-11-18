classdef Beam < handle

    properties
        total_length (1, 1) {mustBeNumeric}
        nodes (1, :) Node
        point_loads (1, :) PointLoad
        point_moments (1, :) PointMoment
        members (1, :) Member
    end

    methods
        function obj = Beam(total_length)
            obj.total_length = total_length;
            obj.nodes = Node.empty();
            obj.point_loads = PointLoad.empty();
            obj.point_moments = PointMoment.empty();
            obj.members = Member.empty();
        end

        function obj = add_node(obj, node)
            obj.nodes(end + 1) = node;
        end

        function obj = add_point_load(obj, load)
            obj.point_loads(end + 1) = load;
        end

        function obj = add_point_moment(obj, moment)
            obj.point_moments(end + 1) = moment;
        end

        function obj = add_member(obj, member)
            obj.members(end + 1) = member;
        end

    end

end