classdef BeeTSP < Bee
    properties
        routeLen
        coords
        distances
        best_distances
    end
    methods
        function obj = BeeTSP(inp, ns, nb, ne, nrb, nre, iterations)
            obj = obj@Bee(ns, nb, ne, nrb, nre, iterations);
            if isfield(inp, 'routeLen')
                obj.routeLen = inp.routeLen;
                obj.coords = obj.randCoords();
            elseif isfield(inp, 'coords')
                obj.coords = inp.coords;
                obj.routeLen = length(obj.coords);
            else
                error('Invalid input')
            end
            obj.distances = obj.evalDistances();
        end
        
        function value = eval(obj, instance)
            value = 0;            
            for i = 2:length(instance)
                value = value + obj.distances(instance(i-1), instance(i));
            end
            value = value + obj.distances(instance(end), 1);
        end

    function r = random(obj)
        r = [1, randperm(obj.routeLen - 1) + 1];
    end
    
    function coords = randCoords(obj)
        coords = [];
        for i = 1:obj.routeLen
            coords = [coords; randi([0, 100]), randi([0, 100])];
        end
    end

    function distances = evalDistances(obj)
        distances = zeros(obj.routeLen, obj.routeLen);
        for i = 1:obj.routeLen
            for j = i+1:obj.routeLen
                distances(i, j) = sqrt((obj.coords(i, 1) - obj.coords(j, 1))^2 + (obj.coords(i, 2) - obj.coords(j, 2))^2);
                distances(j, i) = distances(i, j);
            end
        end
    end

    function initialRandSolution(obj)
        for iter = 1:obj.ns
            x = obj.random();
            y = obj.eval(x);
            obj.bees = [obj.bees; [x, y]];
        end
        obj.bees = sortrows(obj.bees, obj.routeLen);
        % disp(obj.bees);
    end
    
    function newRoute = mutate(obj, route)
        idx1 = randi([2, obj.routeLen]);
        idx2 = randi([2, obj.routeLen]);

        if idx1 == idx2
            newRoute = obj.mutate(route);
            
        elseif idx1 < idx2
            newRoute = [route(1:idx1-1), fliplr(route(idx1:idx2)), route(idx2+1:end-1)];
        else
            newRoute = [route(1:idx2-1), fliplr(route(idx2:idx1)), route(idx1+1:end-1)];
        end
    end

    function eliteSearch(obj)
        for e = 1:obj.ne
            bestValue = inf;
            bestMutation = [];
            for i = 1:obj.nre
                mutation = obj.mutate(obj.bees(e, :));
                mutationObjective = obj.eval(mutation);
                if mutationObjective < bestValue
                    bestMutation = mutation;
                    bestValue = mutationObjective;
                end
            end
            if bestValue < obj.bees(e, obj.routeLen+1)
                obj.bees(e, :) = [bestMutation, bestValue];
            end
        end
    end

    function bestSearch(obj)
        for b = obj.ne + 2:obj.nb + 1
            bestValue = inf;
            bestMutation = [];
            for i = 1:obj.nrb
                mutation = obj.mutate(obj.bees(b, :));
                mutationObjective = obj.eval(mutation);
                if mutationObjective < bestValue
                    bestMutation = mutation;
                    bestValue = mutationObjective;
                end
            end
            if bestValue < obj.bees(b, obj.routeLen+1)
                obj.bees(b, :) = [bestMutation, bestValue];
            end
        end
    end

    function globalFill(obj)
        for g = obj.nb + 2:length(obj.bees)
            obj.bees(g, :) = [obj.random(), obj.eval(obj.random())];
        end
    end


    function calculateBests(obj)
        obj.bees = sortrows(obj.bees, size(obj.bees, 2));
        obj.best_distances = [obj.best_distances; obj.bees(1, end)];
    end

    function visualize(obj)
        tspRoute = obj.bees(1,1:end-1);
        coords = obj.coords;
        x_coords = coords(:, 1);
        y_coords = coords(:, 2);
    
        % Plot the points
        scatter(x_coords, y_coords, 'blue', 'o', 'DisplayName', 'Cities');
    
        % Plot the TSP route
        for i = 1:length(tspRoute)
            next_i = mod(i, length(tspRoute)) + 1;
            line([x_coords(tspRoute(i)), x_coords(tspRoute(next_i))], ...
                 [y_coords(tspRoute(i)), y_coords(tspRoute(next_i))], 'Color', 'red');
        end
    
        % Highlight the starting point
        hold on;
        scatter(x_coords(tspRoute(1)), y_coords(tspRoute(1)), 'green', 's', 'DisplayName', 'Start');

        % Add labels and title
        bestdistance = obj.bees(1, end);
        titleText = sprintf('TSP Route Visualization - Best Distance: %f', bestdistance);
        title(titleText);
        xlabel('X Coordinate');
        ylabel('Y Coordinate');
    
        % Show the plot
        hold off;
    end
    
    function animate(obj, fig)
        if ~isvalid(fig)
            return;
        end

        clf(fig);

        subplot(1,2,1);

        % Get the current best route and its coordinates
        tspRoute = obj.bees(1,1:end-1);
        coords = obj.coords;
        x_coords = coords(:, 1);
        y_coords = coords(:, 2);

        % Plot the points
        scatter(x_coords, y_coords, 'blue', 'o', 'DisplayName', 'Cities');

        % Plot the TSP route
        for i = 1:length(tspRoute)
            next_i = mod(i, length(tspRoute)) + 1;
            line([x_coords(tspRoute(i)), x_coords(tspRoute(next_i))], ...
                 [y_coords(tspRoute(i)), y_coords(tspRoute(next_i))], 'Color', 'red');
        end

        % Highlight the starting point
        hold on;
        scatter(x_coords(tspRoute(1)), y_coords(tspRoute(1)), 'green', 's', 'DisplayName', 'Start');

        % Add labels and title
        bestdistance = obj.bees(1, end);
        titleText = sprintf('TSP Route Visualization - Best Distance: %f', bestdistance);
        title(titleText);
        xlabel('X Coordinate');
        ylabel('Y Coordinate');

        subplot(1,2,2);
         % Create a subplot for the best distances
        subplot(1, 2, 2);
        plot(obj.best_distances, 'LineWidth', 2);
        title('Best Distance Over Time');
        xlabel('Iteration');
        ylabel('Best Distance');
        grid on;

        % Show the plot
        hold off;

        % Pause for a short time to create the animation effect
        pause(0.001);
    end

    function solve(obj)
        fig = figure;
        obj.initialRandSolution();
        for t = 1:obj.iterations
            obj.eliteSearch();
            obj.bestSearch();
            obj.globalFill();
            obj.calculateBests();
            obj.animate(fig);
        end
        % obj.visualize();
    end

    end
end
