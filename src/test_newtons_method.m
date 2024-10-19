clc;clearvars;

f = @(x) (5/3)*cosd(40) - (5/2)*cosd(x) + (11/6) - cosd(40 - x);
d_f = @(x) (5/2 * sind(x) - sind(40 - x)) * (pi/180);

disp(newtons_method(30, f, d_f))
