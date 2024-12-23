classdef UniformDistributedLoad
    properties (Access=private)
        start_position Point2D
        end_position Point2D
        a {mustBeNumeric}
        b {mustBePositive, mustBeNumeric}
        p1 {mustBeNumeric}
        p2 {mustBeNumeric}
        l_1 {mustBeNumeric}
        l_2 {mustBeNumeric}
    end

    methods (Access=private)
        function forces = fixed_end_forces(obj)
            L = obj.len();
            w = obj.getMagnitude();
            l1 = obj.l_1;
            l2 = obj.l_2;

            FS_b = w*L/2 * (1 - (l1/L^4) * (2*L^3 - 2*l1^2*L + l1^3) - ...
                (l2^3/L^4)*(2*L - l2));

            FS_e = w*L/2 * (1 - (l1^3/L^4)*(2*L - l1) - (l2/L^4)*(2*L^3 - ...
                2*l2^2*L + l2^3));

            forces = [FS_b FS_e];
        end

        function moments = fixed_end_moments(obj)
            L = obj.len();
            w = obj.getMagnitude();
            l1 = obj.l_1;
            l2 = obj.l_2;

            FM_b = w*L^2/12 * (1 - (l1^2/L^4)*(6*L^2 - 8*l1*L + 3*l1^2)- ...
                (l2^3/L^4)*(4*L - 3*l2));

            FM_e = w*L^2/12 * (1 - (l1^3/L^4)*(4*L - 3*l1) - (l2^2/L^4)* ...
                (6*L^2 - 8*l2*L + 3*l2^2));

            moments = [FM_b -1*FM_e];
        end

        function add_fixed_forces(obj, start_node, end_node)
            fixed_end_forces = obj.fixed_end_forces();
            fef = fixed_end_forces(1) + ...
                double(start_node.getFixedEndForce());
            start_node.setFixedEndForce(PointLoad(fef, start_node));

            fef = fixed_end_forces(2) + ...
                double(end_node.getFixedEndForce());
            end_node.setFixedEndForce(PointLoad(fef, end_node));
        end

        function add_fixed_end_moments(obj, start_node, end_node)
            fixed_end_moments = obj.fixed_end_moments();

            fem = fixed_end_moments(1) + ...
                double(start_node.getFixedEndMoment());
            start_node.setFixedEndMoment(PointMoment(fem, ...
                start_node));

            fem = fixed_end_moments(2) + ...
                double(end_node.getFixedEndMoment());
            end_node.setFixedEndMoment(PointMoment(fem, end_node));
        end
    end

    methods
        function obj = UniformDistributedLoad(p1, p2, start_node, end_node, ...
                a, b)
            arguments
                p1 {mustBeNumeric}
                p2 {mustBeNumeric}
                start_node Node
                end_node Node
                a {mustBeNumeric} = start_node.getPosition.x
                b {mustBePositive, mustBeNumeric} = end_node.getPosition.x
            end
            obj.p1 = p1;
            obj.p2 = p2;
            obj.start_position = start_node.getPosition();
            obj.end_position = end_node.getPosition();
            obj.a = a;
            obj.b = b;
            obj.l_1 = obj.a - obj.start_position.x;
            obj.l_2 = obj.end_position.x - obj.b;

            start_support_type = start_node.getSupport().getType();
            end_support_type = end_node.getSupport().getType();

            if start_support_type == SupportType.FREE && ...
               end_support_type == SupportType.FREE
                error("Both Nodes cannot be free")
            end

            obj.add_fixed_forces(start_node, end_node);
            obj.add_fixed_end_moments(start_node, end_node);
            
        end

        function start_position = getStartPosition(obj)
            start_position = obj.start_position;
        end

        function end_position = getEndPosition(obj)
            end_position = obj.end_position;
        end

        function magnitude = getMagnitude(obj, dist)
             if nargin < 2
                 dist = obj.len();
             end

             if dist == obj.len()
                 p2 = obj.p2;
             end

             magnitude = 1 / 2 * (obj.p1 + p2);  

        end

        function len = len(obj)
            len = obj.b - obj.a;
        end

        function r = double(obj)
            r = obj.getMagnitude();d
        end
    end
end