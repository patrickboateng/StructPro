classdef UniformDistributedLoad
    properties
        magnitude double
        start_position Point2D
        end_position Point2D
        a {mustBeNumeric}
        b {mustBePositive, mustBeNumeric}
    end

    properties (Access=private)
        l_1 {mustBeNumeric}
        l_2 {mustBeNumeric}
    end

    methods
        function obj = UniformDistributedLoad(p1, p2, start_node, end_node, ...
                                              a, b)
            arguments
                p1 {mustBeNumeric}
                p2 {mustBeNumeric}
                start_node Node
                end_node Node
                a {mustBeNumeric} = start_node.position.x
                b {mustBePositive, mustBeNumeric} = end_node.position.x
            end
            obj.magnitude = 1/2 * (p1 + p2);
            obj.start_position = start_node.position;
            obj.end_position = end_node.position;
            obj.a = a;
            obj.b = b;
            obj.l_1 = obj.a - obj.start_position.x;
            obj.l_2 = obj.end_position.x - obj.b;

            start_support_type = start_node.support.Type;
            end_support_type = end_node.support.Type;

            if start_support_type == SupportType.FREE && ...
                    end_support_type == SupportType.FREE
                error("Both Nodes cannot be free")
            end

            obj.add_fixed_forces(start_node, end_node);
            obj.add_fixed_end_moments(start_node, end_node);            
        end

        function add_fixed_forces(obj, start_node, end_node)
            fixed_end_forces = obj.fixed_end_forces();
            fixed_end_force = fixed_end_forces(1) + ...
                              start_node.fixed_end_force.magnitude;
            start_node.fixed_end_force = PointLoad(fixed_end_force, ...
                                                   start_node);

            fixed_end_force = fixed_end_forces(2) + ...
                              end_node.fixed_end_force.magnitude;
            end_node.fixed_end_force = PointLoad(fixed_end_force, ...
                                                 end_node);
        end

        function add_fixed_end_moments(obj, start_node, end_node)
            fixed_end_moments = obj.fixed_end_moments();

            fixed_end_moment = fixed_end_moments(1) + ...
                               start_node.fixed_end_moment.magnitude;
            start_node.fixed_end_moment = PointMoment(fixed_end_moment, ...
                                                      start_node);

            fixed_end_moment = fixed_end_moments(2) + ...
                               end_node.fixed_end_moment.magnitude;
            end_node.fixed_end_moment = PointMoment(fixed_end_moment, ...
                                                    end_node);
        end

        function len = len(obj)
            len = obj.b - obj.a;
        end

        function forces = fixed_end_forces(obj)
            L = obj.len();
            w = obj.magnitude;
            l_1 = obj.l_1;
            l_2 = obj.l_2;
            
            FS_b = w*L/2 * (1 - (l_1/L^4) * (2*L^3 - 2*l_1^2*L + l_1^3) - ...
                   (l_2^3/L^4)*(2*L - l_2));
            
            FS_e = w*L/2 * (1 - (l_1^3/L^4)*(2*L - l_1) - (l_2/L^4)*(2*L^3 - ...
                   2*l_2^2*L + l_2^3));

            forces = [FS_b FS_e];
        end

        function moments = fixed_end_moments(obj)
            L = obj.len();
            w = obj.magnitude;
            l_1 = obj.l_1;
            l_2 = obj.l_2;

            FM_b = w*L^2/12 * (1 - (l_1^2/L^4)*(6*L^2 - 8*l_1*L + 3*l_1^2)- ...
                   (l_2^3/L^4)*(4*L - 3*l_2));

            FM_e = w*L^2/12 * (1 - (l_1^3/L^4)*(4*L - 3*l_1) - (l_2^2/L^4)* ...
                   (6*L^2 - 8*l_2*L + 3*l_2^2));

            moments = [FM_b -1*FM_e];
        end
    end
end