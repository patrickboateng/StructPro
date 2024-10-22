function testA = testNonLinearNumericalMethods
testA = functiontests(localfunctions);
end

function testBisectionMethod(testcase)
fn = testcase.TestData.fn;
tol = testcase.TestData.tol;
expected = testcase.TestData.expected;
res = bisection_method(30, 40, fn);
verifyTrue(testcase, abs(res - expected) < tol)
end

function testNewtonRaphsonMethod(testcase)
fn = testcase.TestData.fn;
diff_fn = testcase.TestData.diff_fn;
tol = testcase.TestData.tol;
expected = testcase.TestData.expected;
res = newtons_method(30, fn, diff_fn);
verifyTrue(testcase, abs(res - expected) < tol)
end

function testSecantMethod(testcase)
fn = testcase.TestData.fn;
tol = testcase.TestData.tol;
expected = testcase.TestData.expected;
res = secant_method(30, 40, fn);
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