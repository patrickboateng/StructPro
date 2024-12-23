classdef Beam2D < handle
    properties (Access=private)
        total_length (1, 1) {mustBeNumeric}
        nodes (1, :) BmNode
        members (1, :) BmMember
        point_loads (1, :) PointLoad
        point_moments (1, :) PointMoment
        distributed_loads (1, :) UniformDistributedLoad
    end

    properties
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
            obj.point_loads(end + 1) = node.getPointLoad();
            obj.point_moments(end + 1) = node.getPointMoment();
        end

        function obj = add_member(obj, member)
            obj.members(end + 1) = member;
        end

        function obj = add_nodes(obj, nodes)
            arguments
                obj
                nodes (1, :) BmNode
            end

            for i=1:numel(nodes)
                obj.add_node(nodes(i));
            end
        end

        function obj = add_members(obj, members)
            arguments
                obj
                members (1, :) BmMember
            end

            for i=1:numel(members)
                obj.add_member(members(i));
            end
        end

        function len = getLength(obj)
            len = obj.total_length;
        end

        function nodes = getNodes(obj)
            nodes = obj.nodes;
        end

        function members = getMembers(obj)
            members = obj.members;
        end

        function point_loads = getPointLoads(obj)
            point_loads = obj.point_loads;
        end

        function point_moments = getPointMoments(obj)
            point_moments = obj.point_moments();
        end

        function distributed_loads = getDistributedLoads(obj)
            distributed_loads = obj.distributed_loads;
        end

        function [x, shear_force] = calc_shear_force(obj)
            x = linspace(0, obj.total_length, 1000);
            num_of_nodes = numel(obj.nodes);
            num_of_dist_loads = numel(obj.distributed_loads);
            shear_force = zeros(size(x));

            if ~obj.is_solved
                obj.solve();
            end

            for i = 1:numel(x)
                current_x = x(i);
                V = 0;

                % Add contribution from point loads
                for j = 1:num_of_nodes
                    node = obj.nodes(j);
                    if node.getPosition().x <= current_x
                        V = V + double(node.getReactionForce());
                        V = V + double(node.getPointLoad());
                    end
                end

                % Add contribution from distributed loads
                for k = 1:num_of_dist_loads
                    distributed_load = obj.distributed_loads(k);
                    x_start = distributed_load.getStartPosition().x;
                    x_end = distributed_load.getEndPosition().x;

                    if current_x > x_start && current_x <= x_end
                        w = distributed_load.getMagnitude();
                        length_covered = current_x - x_start;
                        V = V + w * length_covered;
                    end
                end

                shear_force(i) = V;

            end
        end

        function [x, bending_moment] = calc_bending_moment(obj)
            node = obj.nodes(1);
            [x, shear_force] = obj.calc_shear_force();
            bending_moment = cumtrapz(x, shear_force);
            bending_moment = bending_moment - double(node.getReactionMoment());
        end

        function [x, slope] = calc_slope(obj)
            member = obj.members(1);
            node = obj.nodes(1);
            E = member.getSection().getE();
            I = member.getSection().getI();
            [x, bending_moment] = obj.calc_bending_moment();
            slope = cumtrapz(x, bending_moment ./ (E * I));
            slope = slope + node.getRotation();
        end

        function [x, deflection] = calc_deflection(obj)
            node = obj.nodes(1);
            [x, slope] = obj.calc_slope();
            deflection = cumtrapz(x, slope);
            deflection = deflection + node.getDisplacement();
        end

        function solve(obj)            
            num_of_nodes = numel(obj.getNodes());
            num_of_elements = num_of_nodes - 1;
            numDOF = num_of_nodes * 2;

            ext_force_vec = zeros(numDOF, 1);
            disp_vec = zeros(numDOF, 1);

            % Global stiffness matrix
            G_K = zeros(numDOF);

            for i=1:num_of_elements
                mem = obj.members(i);
                % Local stiffness matrix
                L_k = mem.stiffness_matrix();

                % Local stiffness matrix location in Global stiffness
                % matrix
                idx_i = (i-1) * 2 + 1;
                idx_j = idx_i + 3;

                % Add element stiffness to global stiffness
                G_K(idx_i:idx_j, idx_i:idx_j) = G_K(idx_i:idx_j, ...
                    idx_i:idx_j) + L_k;
            end

            % Building the force vector
            for i=1:num_of_nodes
                frc_idx = i * 2 - 1;
                mom_idx = frc_idx + 1;
                node = obj.nodes(i);
                support = node.getSupport();

                ext_force_vec(frc_idx) = node.getPointLoad() + ...
                    node.getFixedEndForce();
                ext_force_vec(mom_idx) = node.getPointMoment() + ...
                    node.getFixedEndMoment();

                disp_vec(frc_idx) = support.UY;
                disp_vec(mom_idx) = support.UZ;
            end

            freeDOF = find(disp_vec);

            K_ff = G_K(freeDOF, freeDOF);

            F_f = ext_force_vec(freeDOF);

            disp_vec(freeDOF) = K_ff \ F_f;

            reaction_forces = G_K * disp_vec - ext_force_vec;

            for i=1:num_of_nodes
                frc_idx = i * 2 - 1;
                mom_idx = frc_idx + 1;
                node = obj.nodes(i);
                node.setReactionForce(PointLoad(reaction_forces(frc_idx), node));                
                node.setReactionMoment(PointMoment(reaction_forces(mom_idx), node));
                node.setDisplacement(disp_vec(frc_idx));
                node.setRotation(disp_vec(mom_idx));
            end
            obj.is_solved = true;
        end
    end
end
