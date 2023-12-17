
classdef Bee < handle
    properties
        ns
        nb
        ne
        nrb
        nre
        iterations
        bees
    end
    methods
        function obj = Bee(ns, nb, ne, nrb, nre, iterations)
            obj.ns = ns;
            obj.nb = nb;
            obj.ne = ne;
            obj.nrb = nrb;
            obj.nre = nre;
            obj.iterations = iterations;
            obj.bees = [];
        end
        function solve(obj)
            obj.initialRandSolution();
            for t = 1:obj.iterations
                obj.eliteSearch();
                obj.bestSearch();
                obj.globalFill();
                obj.calculateBests();
            end
        end
        function eliteSearch(obj)
            % Implement the method here
        end
        function globalFill(obj)
            % Implement the method here
        end
        function bestSearch(obj)
            % Implement the method here
        end
        function mutate(obj, instance)
            % Implement the method here
        end
        function eval(obj, instance)
            % Implement the method here
        end
        function randSolution(obj)
            % Implement the method here
        end
        function initialRandSolution(obj)
            % Implement the method here
        end
        function calculateBests(obj)
            % Implement the method here
        end
    end
end