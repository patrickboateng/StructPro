clc, clearvars;

disp(bisection_method(30, 40, @f));

function R = f(x)
    R = (5/3)*cosd(40) - (5/2)*cosd(x) + (11/6) - cosd(40 - x);
end