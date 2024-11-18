classdef Support
    properties
        RX {mustBeNumericOrLogical}
        RY {mustBeNumericOrLogical}
        RM {mustBeNumericOrLogical}
    end

    methods
        function obj = Support(rx, ry, rm)
            obj.RX = rx;
            obj.RY = ry;
            obj.RM = rm;
        end

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