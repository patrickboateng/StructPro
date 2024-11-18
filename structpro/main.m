clc;clearvars;

node_1 = Node(1, 0, 0, 0, 0, 1, 1, 1);
node_2 = Node(2, 5, 0, -5, 10, 0, 0, 0);
node_3 = Node(3, 10, 0, 0, 0, 1, 1, 1);
% 
section = RectangularSection(0.2, 0.4, 200e9);
% 
member_1 = Member(1, node_1, node_2, section);
member_2 = Member(1, node_2, node_3, section);
% 
beam = Beam(10);

beam.add_node(node_1);
beam.add_node(node_2);
beam.add_node(node_3);

% 
beam.add_member(member_1);
beam.add_member(member_2);
% 

% node_1 = Node(1, 0, 0, 0, 0, 1, 1, 0);
% node_2 = Node(2, 2, 0, 0, 0, 0, 1, 0);
% node_3 = Node(3, 4, 0, -5, 0, 0, 0, 0);
% 
% member_1 = Member(1, node_1, node_2, section);
% member_2 = Member(2, node_2, node_3, section);
% 
% beam = Beam(4);
% 
% beam.add_node(node_1);
% beam.add_node(node_2);
% beam.add_node(node_3);
% 
% beam.add_member(member_1);
% beam.add_member(member_2);

Solver.solve(beam)

