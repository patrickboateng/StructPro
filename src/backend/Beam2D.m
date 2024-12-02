classdef Beam2D < handle

    properties
        total_length (1, 1) {mustBeNumeric}
        nodes (1, :) Node
        members (1, :) Member
    end

    methods
        function obj = Beam2D(total_length)
            obj.total_length = total_length;
            obj.nodes = Node.empty();
            obj.members = Member.empty();
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
                members (1, :) Member
            end
            
            for i=1:length(members)
                obj.add_member(members(i));
            end
        end
    
    end

end