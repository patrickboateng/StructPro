classdef RectangularSection < Section
    methods
        function obj = RectangularSection(b, d, E)  
            arguments
                b {mustBePositive, mustBeNumeric}
                d {mustBePositive, mustBeNumeric}
                E {mustBePositive, mustBeNumeric}
            end
            I = (b * d^3) / 12;
            A = b * d;
            obj@Section(I, A, E);
        end
    end
end