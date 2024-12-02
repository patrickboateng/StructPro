classdef StaticFrame2DSolver

    methods (Static)
        function res = solve(beam)
            arguments
                beam Frame2D
            end

            num_of_nodes = length(beam.nodes);
            num_of_members = length(beam.members);
            numDOF = num_of_nodes * 3;

            ext_force_vec = zeros(numDOF, 1);
            disp_vec = zeros(numDOF, 1);

            % Global stiffness matrix
            K = zeros(numDOF);

            for i=1:num_of_members
                mem = beam.members(i);
                mem_k = mem.stiffness_matrix();

                % disp(mem_k)

                idx_i = (i-1) * 3 + 1;
                idx_j = idx_i + 5;

                % Add element stiffness to global stiffness
                K(idx_i:idx_j, idx_i:idx_j) = K(idx_i:idx_j, idx_i:idx_j)...
                                              + mem_k;
            end

            % Building the force vector
            for i=1:num_of_nodes
                lat_frc_idx = i * 3 - 2;
                ver_frc_idx = lat_frc_idx + 1;
                mom_idx = lat_frc_idx + 2;

                node = beam.nodes(i);
                support = node.support;

                ext_force_vec(lat_frc_idx) = node.lat_point_load.magnitude;
                ext_force_vec(ver_frc_idx) = node.ver_point_load.magnitude;
                ext_force_vec(mom_idx) = node.point_moment.magnitude;

                disp_vec(lat_frc_idx) = support.UX;
                disp_vec(ver_frc_idx) = support.UY;
                disp_vec(mom_idx) = support.UZ;
            end

            freeDOF = find(disp_vec);

            K_ff = K(freeDOF, freeDOF);

            F_f = ext_force_vec(freeDOF);

            disp_vec(freeDOF) = gauss_elimination(K_ff, F_f);

            reaction_forces = K * disp_vec - ext_force_vec;

            res = reaction_forces;
            disp(disp_vec)
        end

    end

end
