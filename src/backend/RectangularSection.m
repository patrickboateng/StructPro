classdef RectangularSection
    properties
        I {mustBePositive, mustBeNumeric}
        E {mustBePositive, mustBeNumeric}
        A {mustBePositive, mustBeNumeric}
    end

    methods
        function obj = RectangularSection(b, d, E)  
            arguments
                b {mustBePositive, mustBeNumeric}
                d {mustBePositive, mustBeNumeric}
                E {mustBePositive, mustBeNumeric}
            end
            obj.I = (b * d^3) / 12;
            obj.A = b * d;
            obj.E = E;
        end
    end
end