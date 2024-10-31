function testA = testNonLinearNumericalMethods
testA = functiontests(localfunctions);
end

function testBisectionMethod(testcase)
fn = testcase.TestData.fn;
tol = testcase.TestData.tol;
expected = testcase.TestData.expected;
res = bisection_method(fn, 30, 40);
verifyTrue(testcase, abs(res - expected) < tol)
end

function testNewtonRaphsonMethod(testcase)
fn = testcase.TestData.fn;
diff_fn = testcase.TestData.diff_fn;
tol = testcase.TestData.tol;
expected = testcase.TestData.expected;
res = newtons_method(fn, diff_fn, 30);
verifyTrue(testcase, abs(res - expected) < tol)
end

function testSecantMethod(testcase)
fn = testcase.TestData.fn;
tol = testcase.TestData.tol;
expected = testcase.TestData.expected;
res = secant_method(fn, 30, 40);

verifyTrue(testcase, abs(res - expected) < tol)

fn = @(t) (300000 / (1 + 30.003*exp(-0.08*t))) - 90000 * exp(-0.045*t) ...
    - 120000;
expected = 39.9878;
res = secant_method(fn, 30, 40, Tol=0.05);

verifyTrue(testcase, abs(res - expected) < tol)
end

function setupOnce(testcase)
testcase.TestData.fn = @(x) (5/3)*cosd(40) - (5/2)*cosd(x) + ...
    (11/6) - cosd(40 - x);
testcase.TestData.diff_fn = @(x) (5/2 * sind(x) - sind(40 - x)) * ...
    (pi/180);
testcase.TestData.expected = 32.0152;
testcase.TestData.tol = 1e-4;
end

