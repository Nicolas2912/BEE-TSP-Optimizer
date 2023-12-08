classdef TSP
    properties
        cities
        distances
    end
    
    methods
        function obj = TSP(cities)
            obj.cities = cities;
            
            % calculate distances between cities
            numCities = length(cities);
            obj.distances = zeros(numCities, numCities);
            for i = 1:numCities
                for j = 1:numCities
                    obj.distances(i, j) = norm(cities(i, :) - cities(j, :));
                end
            end
        end
        
        function plot(obj)
            figure;
            scatter(obj.cities(:, 1), obj.cities(:, 2), 'red', 'filled');
            
            % Connect cities with lines
            hold on;
            plot(obj.cities(:, 1), obj.cities(:, 2), 'Color', [0.7, 0.7, 0.7], 'LineStyle', '--');
            plot([obj.cities(end, 1), obj.cities(1, 1)], [obj.cities(end, 2), obj.cities(1, 2)], 'Color', [0.7, 0.7, 0.7], 'LineStyle', '--');
            
            hold off;
            grid on;
            axis equal;
            title('TSP Visualization');
            xlabel('X-Axis');
            ylabel('Y-Axis');
        end
        
        function bestRoute = bruteForce(obj)
            numCities = size(obj.cities, 1);
            allPermutations = perms(1:numCities);

            minDistance = inf;
            bestRoute = [];

            disp(['All permutations: ' num2str(size(allPermutations, 1))]);

            for k = 1:size(allPermutations, 1)
                totalDistance = 0;
                for i = 1:numCities - 1
                    totalDistance = totalDistance + obj.distances(allPermutations(k, i), allPermutations(k, i + 1));
                end
                totalDistance = totalDistance + obj.distances(allPermutations(k, end), allPermutations(k, 1));  % Schließe die Rundtour ab

                if totalDistance < minDistance
                    minDistance = totalDistance;
                    bestRoute = allPermutations(k, :);
                end
            end

            % Sicherstellen, dass die Route geschlossen ist
            bestRoute = [bestRoute, bestRoute(1)];
        end
        
        function plotRoute(obj, route)
            figure;
            scatter(obj.cities(:, 1), obj.cities(:, 2), 'red', 'filled');
            
            % Connect cities with lines (geschlossene Rundtour)
            hold on;
            plot(obj.cities(route, 1), obj.cities(route, 2), 'blue', 'LineStyle', '--', 'LineWidth', 2);
            hold off;
            
            grid on;
            axis equal;
            title('TSP Route');
            xlabel('X-Axis');
            ylabel('Y-Axis');
        end
    end
end
