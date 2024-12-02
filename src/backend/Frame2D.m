classdef Frame2D < handle

    properties
        nodes (1, :) Node
        members (1, :) FrameMember
    end

    methods
        function obj = Frame2D()
            obj.nodes = Node.empty();
            obj.members = FrameMember.empty();
        end

        function obj = add_node(obj, node)
            obj.nodes(end + 1) = node;
        end

        function obj = add_member(obj, member)
            obj.members(end + 1) = member;
        end

        function obj = add_nodes(obj, nodes)
            arguments
                obj
                nodes (1, :) Node
            end

            for i=1:length(nodes)
                obj.add_node(nodes(i));
            end
        end

        function obj = add_members(obj, members)
            arguments
                obj
                members (1, :) FrameMember
            end

            for i=1:length(members)
                obj.add_member(members(i));
            end
        end

    end
end