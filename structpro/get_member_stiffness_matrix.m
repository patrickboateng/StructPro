function res = get_member_stiffness_matrix(member)
arguments
    member Member
end

m_len = member.end_node.position.x - member.start_node.position.x;
E = member.section.E;
I = member.section.I;

k = (E * I) / m_len^3;

m_stiffness = [12 6*m_len -12 6*m_len; ...
              6*m_len 4*m_len^2 -6*m_len 2*m_len^2; ...
              -12 -6*m_len 12 -6*m_len; ...
              6*m_len 2*m_len^2 -6*m_len 4*m_len^2];

% m_stiffness = m_stiffness .* k;

res = m_stiffness;
end