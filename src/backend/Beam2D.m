classdef Beam2D < handle

    properties
        total_length (1, 1) {mustBeNumeric}
        nodes (1, :) BmNode
        members (1, :) BmMember
        point_loads (1, :) PointLoad
        point_moments (1, :) PointMoment
        distributed_loads (1, :) UniformDistributedLoad

        soln
        is_solved
    end

    methods
        function obj = Beam2D(total_length)
            obj.total_length = total_length;
            obj.nodes = BmNode.empty();
            obj.members = BmMember.empty();
            obj.point_loads = PointLoad.empty();
            obj.point_moments = PointMoment.empty();
            obj.distributed_loads = UniformDistributedLoad.empty();
            obj.is_solved = false;
        end

        function obj = add_distributed_load(obj, distributed_load)
            obj.distributed_loads(end + 1) = distributed_load;
        end

        function obj = add_node(obj, node)
            obj.nodes(end + 1) = node;
            obj.point_loads(end + 1) = node.point_load;
            obj.point_moments(end + 1) = node.point_moment;
        end

        function obj = add_member(obj, member)
            obj.members(end + 1) = member;
        end

        function obj = add_nodes(obj, nodes)
            arguments
                obj
                nodes (1, :) BmNode
            end

            for i=1:length(nodes)
                obj.add_node(nodes(i));
            end
        end

        function obj = add_members(obj, members)
            arguments
                obj
                members (1, :) BmMember
            end

            for i=1:length(members)
                obj.add_member(members(i));
            end
        end

        function reactions = get_reactions(obj)
            reactions = zeros(size(obj.nodes));

            for i=1:length(obj.nodes)
                frc_idx = i * 2 - 1;
                reactions(i) = obj.soln.Reactions(frc_idx);
            end
        end

        function [x, shear_force] = calc_shear_force(obj)
            x = linspace(0, obj.total_length, 1000);
            num_of_nodes = length(obj.nodes);

            num_of_dist_loads = length(obj.distributed_loads);

            shear_force = zeros(size(x));

            if ~obj.is_solved
                StaticBeam2DSolver.solve(obj);
            end

            reactions = obj.get_reactions();

            for i = 1:length(x)
                current_x = x(i);
                V = 0;

                % Add contribution from point loads
                for j = 1:num_of_nodes
                    if obj.nodes(j).position.x <= current_x
                        V = V + reactions(j);
                        V = V + obj.point_loads(j).magnitude;
                    end
                end

                % Add contribution from distributed loads
                for k = 1:num_of_dist_loads
                    distributed_load = obj.distributed_loads(k);
                    x_start = distributed_load.start_position.x;
                    x_end = distributed_load.end_position.x;

                    if current_x > x_start && current_x <= x_end
                        w = distributed_load.magnitude;
                        lengthCovered = current_x - x_start;
                        V = V + w * lengthCovered;
                    end
                end

                shear_force(i) = V; 
            end
        end

    end

end