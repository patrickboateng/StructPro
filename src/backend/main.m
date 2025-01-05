clc;clearvars;

section = RectangularSection();
section.setI(1.000E-04);
section.setA(1.000E-02);

beam = Beam2D(11);

node_1 = BmNode(1, 0, 0, 0, 0, 1, 1, 1);
node_2 = BmNode(2, 2, 0, -150, 0, 0, 0, 0);
node_3 = BmNode(3, 4, 0, 0, 0, 0, 1, 0);
node_4 = BmNode(4, 7, 0, 0, 0, 0, 1, 0);
node_5 = BmNode(5, 11, 0, 0, 0, 1, 1, 1);

elem_1 = BmMember(1, node_1, node_2, section);
elem_2 = BmMember(2, node_2, node_3, section);
elem_3 = BmMember(3, node_3, node_4, section);
elem_4 = BmMember(4, node_4, node_5, section);

udl = UniformDistributedLoad(-37.5, -37.5, node_4, node_5);

beam.add_nodes([node_1, node_2, node_3, node_4, node_5]);
beam.add_members([elem_1, elem_2, elem_3, elem_4]);
beam.add_distributed_load(udl);

% beam = Beam2D(10);
% node_1 = BmNode(1, 0,  0,  0, 0, 1, 1, 1);
% node_2 = BmNode(2, 10, 0,  0, 0, 0, 0, 0);
% member_1 = BmMember(1, node_1, node_2, section);
% beam.add_nodes([node_1, node_2]);
% beam.add_members(member_1);
% 
% udl = UniformDistributedLoad(-10, -10, node_1, node_2);
% beam.add_distributed_load(udl);

beam.solve();

[x, bm] = beam.calc_bending_moment();
[~, sf] = beam.calc_shear_force();
[~, sl] = beam.calc_slope();
[~, df] = beam.calc_deflection();

subplot(4, 1, 1)
area(x, sf)
subplot(4, 1, 2)
area(x, bm)
subplot(4, 1, 3)
area(x, sl)
subplot(4, 1, 4)
area(x, df)
