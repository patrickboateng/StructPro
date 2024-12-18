classdef Section
    properties (SetAccess=immutable)
        I {mustBeNumeric}
        A {mustBeNumeric}
        E {mustBeNumeric}
    end

    methods
        function obj = Section(I, A, E)
            obj.I = I;
            obj.A = A;
            obj.E = E;
        end
    end
end