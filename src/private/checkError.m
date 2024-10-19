function checkError(new_error, old_error)
arguments
    new_error
    old_error
end
if new_error > old_error
    warning("Solution is not converging.")
end
end