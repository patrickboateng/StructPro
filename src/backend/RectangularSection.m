classdef RectangularSection < Section
    methods
        function obj = RectangularSection(b, d, E)  
            arguments
                b {mustBePositive, mustBeNumeric} = 0.1
                d {mustBePositive, mustBeNumeric} = 0.1
                E {mustBePositive, mustBeNumeric} = 200e6
            end
            I = (b * d^3) / 12;
            A = b * d;
            obj@Section(I, A, E);
        end
    end
end