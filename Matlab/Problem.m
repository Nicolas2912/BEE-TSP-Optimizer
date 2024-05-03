classdef Problem < handle
    properties
    end
    methods
        function random(obj)
            % creates a random instance
            % needs to be implemented in child
        end
        function mutate(obj, instance)
            % mutates a specific instance
            % needs to be implemented in child
        end
        function eval(obj, instance)
            % evaluates a specific instance
            % needs to be implemented in child
        end
        function animate(obj, fig, iteration, solution, objective)
            % evaluates a specific instance
            % needs to be implemented in child
        end
        function visualize(obj, solution, objective)
            % evaluates a specific instance
            % needs to be implemented in child
        end
    end
end