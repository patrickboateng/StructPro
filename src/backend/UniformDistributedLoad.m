classdef UniformDistributedLoad
    properties
        magnitude double
        start double
        end_ double
    end

    methods
        function obj = UniformDistributedLoad(magnitude, start, end_)
            obj.magnitude = magnitude;
            obj.start = start;
            obj.end_ = end_;
        end
    end
end