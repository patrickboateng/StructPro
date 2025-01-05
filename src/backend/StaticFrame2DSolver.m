classdef StaticFrame2DSolver

    methods (Static)
        function res = solve(frame)
            arguments
                frame Frame2D
            end

            num_of_nodes = length(frame.nodes);
            num_of_elements = num_of_nodes - 1;
            numDOF = num_of_nodes * 3;

            ext_force_vec = zeros(numDOF, 1);
            disp_vec = zeros(numDOF, 1);

            % Global stiffness matrix
            G_K = zeros(numDOF);

            for i=1:num_of_elements
                mem = frame.members(i);
                L_k = mem.stiffness_matrix();

                idx_i = (i-1) * 3 + 1;
                idx_j = idx_i + 5;

                % Add element stiffness to global stiffness
                G_K(idx_i:idx_j, idx_i:idx_j) = G_K(idx_i:idx_j, idx_i:idx_j)...
                                              + L_k;
            end

            % Building the force vector
            for i=1:num_of_nodes
                lat_frc_idx = i * 3 - 2;
                ver_frc_idx = lat_frc_idx + 1;
                mom_idx = lat_frc_idx + 2;

                node = frame.nodes(i);
                support = node.support;

                ext_force_vec(lat_frc_idx) = node.lat_point_load.magnitude;
                ext_force_vec(ver_frc_idx) = node.ver_point_load.magnitude;
                ext_force_vec(mom_idx) = node.point_moment.magnitude;

                disp_vec(lat_frc_idx) = support.UX;
                disp_vec(ver_frc_idx) = support.UY;
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
