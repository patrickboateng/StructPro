classdef Solver

    methods (Static)
        function res = solve(beam)
            arguments
                beam Beam
            end

            num_of_nodes = length(beam.nodes);
            num_of_members = length(beam.members);
            numDOF = num_of_nodes * 2;

            K = zeros(numDOF);

            for i=1:num_of_members
                mem_k = get_member_stiffness_matrix(beam.members(i));
                % K(i:4, i:4) = K(i:4, i:4) + mem_k;
                % break

                idx_i = (i-1) * 2 + 1;
                idx_j = idx_i + 3;

                % Add element stiffness to global stiffness
                K(idx_i:idx_j, idx_i:idx_j) = K(idx_i:idx_j, idx_i:idx_j)...
                                              + mem_k;
            end

            F_vec = zeros(numDOF, 1);

            U_vec = zeros(numDOF, 1);

            for i=1:num_of_nodes
                f_idx = i * 2 - 1;
                m_idx = f_idx + 1;
                node = beam.nodes(i);
                support_type = node.support.type();
                
                F_vec(f_idx) = node.point_load.magnitude;
                F_vec(m_idx) = node.point_moment.magnitude;

                if support_type == SupportType.FIXED
                    U_vec(f_idx) = 0;
                    U_vec(m_idx) = 0;
                end

                if support_type == SupportType.PINNED
                    U_vec(f_idx) = 0;
                    U_vec(m_idx) = 1;
                end

                if support_type == SupportType.FREE
                    U_vec(f_idx) = 1;
                    U_vec(m_idx) = 1;
                end




            end

            res = U_vec;
            

        end

    end

end