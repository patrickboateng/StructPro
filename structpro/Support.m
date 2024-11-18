classdef Support
    properties (Access = private)
        RX {mustBeNumericOrLogical}
        RY {mustBeNumericOrLogical}
        RM {mustBeNumericOrLogical}
    end

    properties
        UX {mustBeNumericOrLogical}
        UY {mustBeNumericOrLogical}
        UZ {mustBeNumericOrLogical}
        Type SupportType
    end

    methods
        function obj = Support(rx, ry, rm)
            obj.RX = rx;
            obj.RY = ry;
            obj.RM = rm;

            obj.UX = 1 - rx;
            obj.UY = 1 - ry;
            obj.UZ = 1 - rm;

            obj.Type = obj.type();
    
        end

    end

    methods (Access = private)

        function ret_val = type(obj)
            if  obj.RX && obj.RY && obj.RM 
                ret_val = SupportType.FIXED;
            elseif obj.RX && obj.RY
                ret_val = SupportType.PINNED;
            elseif obj.RX || obj.RY
                ret_val = SupportType.ROLLER;
            else
                ret_val = SupportType.FREE;
            end
        end

    end

end