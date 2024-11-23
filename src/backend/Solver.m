classdef Solver

    methods (Static)
        function res = solve(beam)
            arguments
                beam Beam
            end

            num_of_nodes = length(beam.nodes);
            num_of_members = length(beam.members);
            numDOF = num_of_nodes * 2;

            F_vec = zeros(numDOF, 1);
            U_vec = zeros(numDOF, 1);

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

            for i=1:num_of_nodes
                f_idx = i * 2 - 1;
                m_idx = f_idx + 1;
                node = beam.nodes(i);
                support = node.support;

                F_vec(f_idx) = node.point_load.magnitude + node.fixed_end_force.magnitude;
                F_vec(m_idx) = node.point_moment.magnitude + node.fixed_end_moment.magnitude;

                U_vec(f_idx) = support.UY;
                U_vec(m_idx) = support.UZ;
            end

            freeDOF = find(U_vec);

            K_ff = K(freeDOF, freeDOF);

            F_f = F_vec(freeDOF);

            U_vec(freeDOF) = gauss_elimination(K_ff, F_f);

            R = K * U_vec - F_vec;

            res = struct("Displacements", U_vec, "Reactions", R, ...
                "ForceVector", F_vec);
        end

    end

end