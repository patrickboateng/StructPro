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


beam = StaticSolver2D.solve(beam);

for i=1:length(beam.nodes)
    disp([i beam.nodes(i).rotation])
end

