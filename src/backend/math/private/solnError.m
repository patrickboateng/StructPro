function err = solnError(newSoln, oldSoln)
arguments
    newSoln 
    oldSoln 
end
err = max(abs((newSoln - oldSoln) ./ newSoln)) * 100;
end