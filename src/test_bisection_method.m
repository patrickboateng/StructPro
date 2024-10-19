clc, clearvars;

f = @(x) (5/3)*cosd(40) - (5/2)*cosd(x) + (11/6) - cosd(40 - x);

disp(bisection_method(30, 40, @f));
