classdef StaticSolver2D

    methods (Static)
        function res = solve(beam)
            arguments
                beam Beam2D
            end

            num_of_nodes = length(beam.nodes);
            num_of_members = length(beam.members);
            numDOF = num_of_nodes * 2;

            ext_force_vec = zeros(numDOF, 1);
            disp_vec = zeros(numDOF, 1);

            % Global stiffness matrix
            K = zeros(numDOF);

            for i=1:num_of_members
                mem = beam.members(i);
                mem_k = mem.stiffness_matrix();

                idx_i = (i-1) * 2 + 1;
                idx_j = idx_i + 3;

                % Add element stiffness to global stiffness
                K(idx_i:idx_j, idx_i:idx_j) = K(idx_i:idx_j, idx_i:idx_j)...
                    + mem_k;

                fixed_end_forces = mem.fixed_end_forces();
                fixed_end_moments = mem.fixed_end_moments();

                mem.start_node.fixed_end_force = PointLoad( ...
                    fixed_end_forces(1), mem.start_node);
                mem.start_node.fixed_end_moment = PointMoment( ...
                    fixed_end_moments(1), mem.start_node);


                mem.end_node.fixed_end_force = PointLoad( ...
                    fixed_end_forces(2), mem.end_node);
                mem.end_node.fixed_end_moment = PointMoment( ...
                    fixed_end_moments(2), mem.end_node);
            end

            % Building the force vector
            for i=1:num_of_nodes
                frc_idx = i * 2 - 1;
                mom_idx = frc_idx + 1;
                node = beam.nodes(i);
                support = node.support;

                ext_force_vec(frc_idx) = node.point_load.magnitude + node.fixed_end_force.magnitude;
                ext_force_vec(mom_idx) = node.point_moment.magnitude + node.fixed_end_moment.magnitude;

                disp_vec(frc_idx) = support.UY;
                disp_vec(mom_idx) = support.UZ;
            end

            freeDOF = find(disp_vec);

            K_ff = K(freeDOF, freeDOF);

            F_f = ext_force_vec(freeDOF);

            disp_vec(freeDOF) = gauss_elimination(K_ff, F_f);

            reaction_forces = K * disp_vec - ext_force_vec;

            % coverting displacements/rotations to mm
            disp_vec = disp_vec .* 1000;

            for i=1:num_of_nodes
                frc_idx = i * 2 - 1;
                mom_idx = frc_idx + 1;
                node = beam.nodes(i);
                node.reaction_force = PointLoad(reaction_forces(frc_idx), node);
                node.reaction_moment = PointMoment(reaction_forces(mom_idx), node);
                node.displacement = disp_vec(frc_idx);
                node.rotation = disp_vec(mom_idx);
            end

            res = beam;

        end

    end

end