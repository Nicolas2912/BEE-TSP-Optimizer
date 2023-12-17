
classdef Bee < handle
    properties
        ns
        nb
        ne
        nrb
        nre
        iterations
        bees
        best_objectives
        animation
        problem 
    end
    methods
        function obj = Bee(ns, nb, ne, nrb, nre, iterations, animation, problem)
            obj.ns = ns;
            obj.nb = nb;
            obj.ne = ne;
            obj.nrb = nrb;
            obj.nre = nre;
            obj.iterations = iterations;
            obj.bees = [];
            obj.problem = problem;
            obj.animation = animation;
        end
        function solve(obj)
            fig = figure;
            tic;
            obj.initialRandSolution();
            for t = 1:obj.iterations
                obj.eliteSearch();
                obj.bestSearch();
                obj.globalFill();
                obj.calculateBests();
                if obj.animation
                    obj.problem.animate(fig, t, obj.bees(1, 1:end-1), obj.bees(1, end), obj.best_objectives);
                end
            end
            elapsedTime = toc; 
            fprintf('Iterations: %.0f\n', obj.iterations)
            fprintf('Total elapsed time: %.2f seconds\n', elapsedTime);
            best_solution = obj.bees(1, 1:end-1);
            fprintf('Best solution: %s\n', mat2str(best_solution));
            best_objective = obj.bees(1, end);
            fprintf('Best objective: %.3f\n', best_objective);
            if ~ obj.animation
                obj.problem.visualize(best_solution, best_objective);
            end
        end
        function eliteSearch(obj)
            for e = 1:obj.ne
                bestValue = inf;
                bestMutation = [];
                for i = 1:obj.nre
                    mutation = obj.problem.mutate(obj.bees(e, :));
                    mutationObjective = obj.problem.eval(mutation);
                    if mutationObjective < bestValue
                        bestMutation = mutation;
                        bestValue = mutationObjective;
                    end
                end

                if bestValue < obj.bees(e, size(obj.bees, 2))
                    obj.bees(e, :) = [bestMutation, bestValue];
                end
            end
        end
        function bestSearch(obj)
            for b = obj.ne + 2:obj.nb + 1
                bestValue = inf;
                bestMutation = [];
                for i = 1:obj.nrb
                    mutation = obj.problem.mutate(obj.bees(b, :));
                    mutationObjective = obj.problem.eval(mutation);
                    if mutationObjective < bestValue
                        bestMutation = mutation;
                        bestValue = mutationObjective;
                    end
                end
                if bestValue < obj.bees(b, size(obj.bees, 2))
                    obj.bees(b, :) = [bestMutation, bestValue];
                end
            end
        end
        function globalFill(obj)
            for g = obj.nb + 2:length(obj.bees)
                obj.bees(g, :) = [obj.problem.random(), obj.problem.eval(obj.problem.random())];
            end
        end
        function calculateBests(obj)
            obj.bees = sortrows(obj.bees, size(obj.bees, 2));
            obj.best_objectives= [obj.best_objectives; obj.bees(1, end)];
        end
        function initialRandSolution(obj)
            for iter = 1:obj.ns
                x = obj.problem.random();
                y = obj.problem.eval(x);
                obj.bees = [obj.bees; [x, y]];
            end
            obj.bees = sortrows(obj.bees, size(obj.bees, 2));
        end
    end
end