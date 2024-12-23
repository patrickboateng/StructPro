classdef Section < handle
    properties (Access=private)
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

        function I = getI(obj)
            I = obj.I;
        end

        function setI(obj, val)
            obj.I = val;
        end
        
        function A = getA(obj)
            A = obj.A;
        end

        function setA(obj, val)
            obj.A = val;
        end

        function E = getE(obj)
            E = obj.E;
        end

        function setE(obj, val)
            obj.E = val;
        end
    end
end