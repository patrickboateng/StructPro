classdef StaticBeam2DSolver

    methods (Static)
        function res = solve(beam)
            arguments
                beam Beam2D
            end

            num_of_nodes = length(beam.nodes);
            num_of_elements = num_of_nodes - 1;
            numDOF = num_of_nodes * 2;

            ext_force_vec = zeros(numDOF, 1);
            disp_vec = zeros(numDOF, 1);

            % Global stiffness matrix
            G_K = zeros(numDOF);

            for i=1:num_of_elements
                mem = beam.members(i);
                % Local stiffness matrix
                L_k = mem.stiffness_matrix();
                
                % Local stiffness matrix location in Global stiffness
                % matrix
                idx_i = (i-1) * 2 + 1;
                idx_j = idx_i + 3;

                % Add element stiffness to global stiffness
                G_K(idx_i:idx_j, idx_i:idx_j) = G_K(idx_i:idx_j, idx_i:idx_j)...
                    + L_k;
            end

            % Building the force vector
            for i=1:num_of_nodes
                frc_idx = i * 2 - 1;
                mom_idx = frc_idx + 1;
                node = beam.nodes(i);
                support = node.support;

                ext_force_vec(frc_idx) = node.point_load.magnitude + ...
                    node.fixed_end_force.magnitude;
                ext_force_vec(mom_idx) = node.point_moment.magnitude + ...
                    node.fixed_end_moment.magnitude;

                disp_vec(frc_idx) = support.UY;
                disp_vec(mom_idx) = support.UZ;
            end

            freeDOF = find(disp_vec);

            K_ff = G_K(freeDOF, freeDOF);

            F_f = ext_force_vec(freeDOF);

            disp_vec(freeDOF) = gauss_elimination(K_ff, F_f);

            reaction_forces = G_K * disp_vec - ext_force_vec;

            res = struct("Displacements", disp_vec, ...
                "Reactions", reaction_forces);
        end

    end

end