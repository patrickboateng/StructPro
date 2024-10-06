clc, clearvars;

a = 30;
b = 40;

disp(bisection_method(a, b, @f));

function R = f(x)
    R = (5/3)*cosd(40) - (5/2)*cosd(x) + (11/6) - cosd(40 - x);
end