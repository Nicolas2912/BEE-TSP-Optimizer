classdef TSP < Problem
    properties
        routeLen
        coords
        distances
    end
    methods
        function obj = TSP(inp)
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
            coords = zeros(obj.routeLen, 2);
            for i = 1:obj.routeLen
                coords(i, :) = [randi([0, 100]), randi([0, 100])];
            end
        end

        function distances = evalDistances(obj)
            deltaX = obj.coords(:, 1) - obj.coords(:, 1)';
            deltaY = obj.coords(:, 2) - obj.coords(:, 2)';
            distances = sqrt(deltaX.^2 + deltaY.^2);
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

        function visualize(obj, solution, objective)
            x_coords = obj.coords(:, 1);
            y_coords = obj.coords(:, 2);
            scatter(x_coords, y_coords, 'blue', 'o', 'DisplayName', 'Cities');
            for i = 1:length(solution)
                next_i = mod(i, length(solution)) + 1;
                line([x_coords(solution(i)), x_coords(solution(next_i))], ...
                     [y_coords(solution(i)), y_coords(solution(next_i))], 'Color', 'red');
            end
            hold on;
            scatter(x_coords(solution(1)), y_coords(solution(1)), 'green', 's', 'DisplayName', 'Start');
            titleText = sprintf('TSP Route Visualization - Best Distance: %f', objective);
            title(titleText);
            xlabel('X Coordinate');
            ylabel('Y Coordinate');
            hold off;
        end

        function animate(obj, fig, iteration, solution, objective, best_objectives)
            if mod(iteration, 100) ~= 0
                return;
            end

            if ~isvalid(fig)
                return;
            end
            clf(fig);
            subplot(1,2,1);
            x_coords = obj.coords(:, 1);
            y_coords = obj.coords(:, 2);
            scatter(x_coords, y_coords, 'blue', 'o', 'DisplayName', 'Cities');
            for i = 1:length(solution)
                next_i = mod(i, length(solution)) + 1;
                line([x_coords(solution(i)), x_coords(solution(next_i))], ...
                     [y_coords(solution(i)), y_coords(solution(next_i))], 'Color', 'red');
            end
            hold on;
            scatter(x_coords(solution(1)), y_coords(solution(1)), 'green', 's', 'DisplayName', 'Start');
            titleText = sprintf('TSP Route Visualization - Best Distance: %f', objective);
            title(titleText);
            xlabel('X Coordinate');
            ylabel('Y Coordinate');
            subplot(1,2,2);
            subplot(1, 2, 2);
            plot(best_objectives, 'LineWidth', 2);
            title('Best Distance Over Time');
            xlabel('Iteration');
            ylabel('Best Distance');
            grid on;
            hold off;
            pause(0.001);
        end

    end
end
