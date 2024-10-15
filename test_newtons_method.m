clc;clearvars;

function R = f(x)
R = (5/3)*cosd(40) - (5/2)*cosd(x) + (11/6) - cosd(40 - x);
end

function R = d_f(x)
R = (5/2 * sind(x) - sind(40 - x)) * (pi/180);
end

disp(newtons_method(30, @f, @d_f))

