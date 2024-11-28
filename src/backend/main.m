clc;clearvars;

section = RectangularSection();
section.I = 108e-6;
section.E = 200e9;

node_1 = Node(1, 0, 0, 0, 0, 1, 1, 1);
node_2 = Node(2, 2, 0, -150, 0, 0, 0, 0);
node_3 = Node(3, 4, 0, 0, 0, 0, 1, 0);
node_4 = Node(4, 7, 0, 0, 0, 0, 1, 0);
node_5 = Node(5, 11, 0, 0, 0, 1, 1, 1);

member_1 = Member(1, node_1, node_2, section, 0);
member_2 = Member(2, node_2, node_3, section, 0);
member_3 = Member(3, node_3, node_4, section, 0);
member_4 = Member(4, node_4, node_5, section, -37.5);

nodes = [node_1, node_2, node_3, node_4, node_5];
members = [member_1, member_2, member_3, member_4];

beam = Beam2D(11);

beam.add_nodes(nodes);
beam.add_members(members);

% beam = Beam(32);
%
% node_1 = Node(1, 0, 0, 0, 0, 1, 1, 1);
% node_2 = Node(2, 24, 0, 0, 0, 0, 1, 0);
% node_3 = Node(3, 28, 0, -12, 0, 0, 0, 0);
% node_4 = Node(4, 32, 0, 0, 0, 0, 1, 0);
%
% beam.add_nodes([node_1, node_2, node_3, node_4]);
%
% member_1 = Member(1, node_1, node_2, section, -2);
% member_2 = Member(2, node_2, node_3, section, 0);
% member_3 = Member(3, node_3, node_4, section, 0);
%
% beam.add_members([member_1, member_2, member_3]);

beam = Beam2D(4);

node_1 = Node(1, 0, 0, 0, 0, 1, 1, 1);
node_2 = Node(2, 2, 0, -8, 0, 0, 0, 0);
node_3 = Node(3, 4, 0, -3, 0, 0, 0, 0);

beam.add_nodes([node_1, node_2, node_3]);

member_1 = Member(1, node_1, node_2, section, 0);
member_2 = Member(2, node_2, node_3, section, 0);

beam.add_members([member_1, member_2]);

beam = StaticSolver2D.solve(beam);

for i=1:length(beam.nodes)
    disp([i beam.nodes(i).reaction_moment.magnitude])
end

function shear_force = calc_shear_force(member, node, start_force)

point_load = node.point_load.magnitude;
reaction_force = node.reaction_force.magnitude;

distributed_load = 0;

if node.id ~= 1
    m_len = member.len();
    distributed_load = member.distributed_load.magnitude;
    distributed_load = distributed_load * m_len;
end


% ext_force = distributed_load;

start_force = start_force + distributed_load;
end_force = start_force + point_load + reaction_force;
shear_force = [start_force, end_force];
shear_force
end

prev_force = 0;
% shear_forces = [];
for i=1:length(beam.members)
    member = beam.members(i);

    if i == 1
        node = member.start_node;
        curr_force = calc_shear_force(member, node, prev_force);
    end

    prev_force = curr_force(2);

    node = member.end_node;
    curr_force = calc_shear_force(member, node, prev_force);
end
