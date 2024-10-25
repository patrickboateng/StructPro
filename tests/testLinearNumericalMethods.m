function testA = testLinearNumericalMethods
testA = functiontests(localfunctions);
end

function testCramersRule(testcase)
A = testcase.TestData.A;
b = testcase.TestData.b;
expected = testcase.TestData.expected;
tol = testcase.TestData.tol;
res = cramers_rule(A, b);
verifyTrue(testcase, all(abs(res - expected) < tol))
end

function testGaussElimination(testcase)
A = testcase.TestData.A;
b = testcase.TestData.b;
expected = testcase.TestData.expected;
tol = testcase.TestData.tol;
res = gauss_elimination(A, b);
verifyTrue(testcase, all(abs(res - expected) < tol))
end

function testGaussJordan(testcase)
A = testcase.TestData.A;
b = testcase.TestData.b;
expected = testcase.TestData.expected;
tol = testcase.TestData.tol;
res = gauss_jordan(A, b);
verifyTrue(testcase, all(abs(res - expected) < tol))
end

function testGaussSeidel(testcase)
A = testcase.TestData.A;
b = testcase.TestData.b;
expected = testcase.TestData.expected;
tol = testcase.TestData.tol;
res = gauss_seidel(A, b);
verifyTrue(testcase, all(abs(res - expected) < tol))
end

function testLUDecomposition(testcase)
A = testcase.TestData.A;
b = testcase.TestData.b;
expected = testcase.TestData.expected;
tol = testcase.TestData.tol;
res = lu_decomposition(A, b);
verifyTrue(testcase, all(abs(res - expected) < tol))
end

function setupOnce(testcase)
testcase.TestData.A = [10 15 5; 15 50 25; 5 25 30];
testcase.TestData.b = [45; 60; 75];
testcase.TestData.expected = [6.5; -2.5; 3.5];
testcase.TestData.tol = 1e-6;
end

