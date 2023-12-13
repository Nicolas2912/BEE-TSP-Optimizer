
classdef BeeTSP < handle
    properties
        max_iter
        n_cities
        cities
        nrb
        nre
        ns
        route_fitness_dict
        best_route
        best_distance
        nb
        ne
        current_sites
        ne_int
        ns_int
        nb_int
    end
    methods
        function obj = BeeTSP(ns, max_iter, n_cities, ne, nb, nrb, nre)
            obj.max_iter = max_iter;
            obj.n_cities = n_cities;
            obj.cities = [[  0.  64.  61.  88.  82.  53.  27.  50.  89.  44.  76.  84.  39.  14.  62.  33.  98.  52.  73.   9.]
 [ 64.   0.  86.  43.  75.  73.  98.   1.  45.  56.  65.   3.  54.  64.  43.  83.   6.  59.  87.  34.]
 [ 61.  86.   0.  84.  75.  59. 100.   5.  40.  88.  22.   7.  85.  26.  31.  30.   2.  35.  57.  84.]
 [ 88.  43.  84.   0.  80.  19.  22.  69.  17.  18.  16.  89.  13.  78.   1.  59.  18.  50.  24.  41.]
 [ 82.  75.  75.  80.   0.  41.  74.  26.  14.  44.  47.  15.  85.  26.   2.  38.  85.  89.  79.   2.]
 [ 53.  73.  59.  19.  41.   0.  98.  94.  50.  63.  92.  54.  67. 100.  86.  34.  83.  62.  49.  91.]
 [ 27.  98. 100.  22.  74.  98.   0.  48.  65.  46.  84.  57.  35.  34.  12.  60.  22.  54. 100.  87.]
 [ 50.   1.   5.  69.  26.  94.  48.   0.  76.  97.   5.  49.  80.  67.  15.   7.  43.  84.  46.  68.]
 [ 89.  45.  40.  17.  14.  50.  65.  76.   0.  25.  49.  16.  78.  26.  74.  13.  46.  22.  79.  99.]
 [ 44.  56.  88.  18.  44.  63.  46.  97.  25.   0.  82.  71.  90.  46.  86.  23.  57.  15.   4.  96.]
 [ 76.  65.  22.  16.  47.  92.  84.   5.  49.  82.   0.  33.  18.  91.  64.   6.  80.  17.  88.  74.]
 [ 84.   3.   7.  89.  15.  54.  57.  49.  16.  71.  33.   0.  54.  53.  20.  38.  35.  90.  94.  93.]
 [ 39.  54.  85.  13.  85.  67.  35.  80.  78.  90.  18.  54.   0.  38.  12.  47.  94.  93.  17.  73.]
 [ 14.  64.  26.  78.  26. 100.  34.  67.  26.  46.  91.  53.  38.   0. 100.  87.  12.   8.  62.  29.]
 [ 62.  43.  31.   1.   2.  86.  12.  15.  74.  86.  64.  20.  12. 100.   0.  41.  48.  21.  63.  86.]
 [ 33.  83.  30.  59.  38.  34.  60.   7.  13.  23.   6.  38.  47.  87.  41.   0.  44.  14.  15.  44.]
 [ 98.   6.   2.  18.  85.  83.  22.  43.  46.  57.  80.  35.  94.  12.  48.  44.   0.  54.  53.  67.]
 [ 52.  59.  35.  50.  89.  62.  54.  84.  22.  15.  17.  90.  93.   8.  21.  14.  54.   0.  57.  67.]
 [ 73.  87.  57.  24.  79.  49. 100.  46.  79.   4.  88.  94.  17.  62.  63.  15.  53.  57.   0.  89.]
 [  9.  34.  84.  41.   2.  91.  87.  68.  99.  96.  74.  93.  73.  29.  86.  44.  67.  67.  89.   0.]]
            obj.nrb = nrb;
            obj.nre = nre;
            obj.ns = arrayfun(@(x) obj.init_random_route(), 1:ns, 'UniformOutput', false);
            obj.route_fitness_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(obj.ns)
                obj.route_fitness_dict(num2str(obj.ns{i})) = obj.get_distance(obj.ns{i});
            end
            keys = obj.route_fitness_dict.keys;
            values = obj.route_fitness_dict.values;
            [~, idx] = sort(cell2mat(values));
            keys = keys(idx);
            obj.best_route = str2num(keys{1});
            obj.best_distance = obj.get_distance(obj.best_route);
            obj.nb = keys(1:nb);
            obj.ne = keys(1:ne);
            for i = 1:length(obj.nb)
                obj.nb{i} = str2num(obj.nb{i});
            end
            for i = 1:length(obj.ne)
                obj.ne{i} = str2num(obj.ne{i});
            end
            obj.current_sites = obj.ns(1:length(obj.nb));
            obj.ne_int = ne;
            obj.ns_int = ns;
            obj.nb_int = nb;
        end

        function route = init_random_route(obj)
            route = randperm(obj.n_cities);
            route = [route, route(1)];
        end

        function distances = init_cities(obj)
            distances = zeros(obj.n_cities, obj.n_cities);
            for i = 1:obj.n_cities
                for j = 1:obj.n_cities
                    if i ~= j
                        rand_dist = randi([1, 100]);
                        distances(i, j) = rand_dist;
                        distances(j, i) = rand_dist;
                    else
                        distances(i, j) = 0;
                    end
                end
            end
        end
    
        function distance = get_distance(obj, route)
            % route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        
            if ischar(route)
                route = eval(route);
            end
        
            distance = 0;
            for i = 1:length(route) - 1
                distance = distance + obj.cities(route(i), route(i + 1));
            end
        end
    
        function plot(obj, route)
            % plot
            if ischar(route)
                route = eval(route);
            end
        
            figure('Position', [10, 10, 800, 800]);
            scatter(obj.cities(:, 1), obj.cities(:, 2), 100, 'filled');
            hold on;
        
            for i = 1:obj.n_cities
                text(obj.cities(i, 1) + 0.1, obj.cities(i, 2) + 0.1, num2str(i-1), 'FontSize', 20);
            end
        
            for i = 1:length(route) - 1
                plot([obj.cities(route(i), 1), obj.cities(route(i + 1), 1)], ...
                     [obj.cities(route(i), 2), obj.cities(route(i + 1), 2)], 'k-');
            end
        
            title_text = sprintf('Best Distance: %.2f\nBest Route: %s', obj.best_distance, mat2str(obj.best_route));
            title(title_text);
        
            grid on;
            hold off;
        end
        
        function new_route = k_opt_exchange(route, k)
            if k < 2 || k >= length(route) - 2
                disp(k);
                error('k must be between 2 and len(route) - 2');
            end
        
            indices_to_swap = randperm(length(route)-2, k) + 1;
        
            new_route = route;
        
            for i = 1:floor(k / 2)
                temp = new_route(indices_to_swap(i));
                new_route(indices_to_swap(i)) = new_route(indices_to_swap(k - i + 1));
                new_route(indices_to_swap(k - i + 1)) = temp;
            end
        end
        
        function new_route = k_opt_exchange_reverse(obj, route, k)
            % Random selection of k different cities
            indices = sort(randperm(length(route)-2, k) + 1);
        
            % Reverse operation
            new_route_reverse = fliplr(route(indices(1):indices(end)));
            new_route = [route(1:indices(1)-1), new_route_reverse, route(indices(end)+1:end)];
        end

        function new_route = two_edge_exchange(obj, route)
            if ischar(route)
                route = eval(route);
            end
        
            % random number from 1 to 3
            n = 2;
            if n == 1
                k = randi([2, length(route) - 3]);
                new_route = obj.k_opt_exchange(route, k);
            elseif n == 2
                k = randi([2, length(route) - 3]);
                new_route = obj.k_opt_exchange_reverse(route, k);
            end
        end
        
        function neighborhoods = neighborhood(obj, route, n)
            neighborhoods = {};
            while length(neighborhoods) < n
                new_neighborhood = obj.two_edge_exchange(route);
                if ~any(cellfun(@(x) isequal(x, new_neighborhood), neighborhoods))
                    neighborhoods{end+1} = new_neighborhood;
                end
            end
        end

        function best_search(obj)
            % 2nd variant
            obj.ne = obj.ns(1:obj.ne_int);
            ne_route_dist_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(obj.ne)
                ne_route_dist_dict(num2str(obj.ne{i})) = obj.get_distance(obj.ne{i});
            end
            keys = ne_route_dist_dict.keys;
            values = ne_route_dist_dict.values;
            [~, idx] = sort(cell2mat(values));
            keys = keys(idx);
        
            for i = 1:length(keys)
                route = str2num(keys{i});
                neighborhood = obj.neighborhood(route, obj.nre);
                neighborhood_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
                for j = 1:length(neighborhood)
                    neighborhood_dict(num2str(neighborhood{j})) = obj.get_distance(neighborhood{j});
                end
                keys_neighborhood = neighborhood_dict.keys;
                values_neighborhood = neighborhood_dict.values;
                [~, idx_neighborhood] = sort(cell2mat(values_neighborhood));
                keys_neighborhood = keys_neighborhood(idx_neighborhood);
        
                obj.ns{i} = str2num(keys_neighborhood{1});
        
                if ne_route_dist_dict(keys{i}) < obj.best_distance
                    obj.best_distance = ne_route_dist_dict(keys{i});
                    obj.best_route = str2num(keys{i});
                    obj.ns{i} = str2num(keys_neighborhood{1});
                end
            end
        
            ns_route_dist_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(obj.ns)
                ns_route_dist_dict(num2str(obj.ns{i})) = obj.get_distance(obj.ns{i});
            end
            keys_ns = ns_route_dist_dict.keys;
            values_ns = ns_route_dist_dict.values;
            [~, idx_ns] = sort(cell2mat(values_ns));
            keys_ns = keys_ns(idx_ns);
            obj.ns = cellfun(@str2num, keys_ns, 'UniformOutput', false);
        end
        
        function elite_search(obj)
            % 2nd variant
            nb_minus_ne = obj.ns(1:(obj.nb_int - obj.ne_int));
            nb_minus_ne_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(nb_minus_ne)
                nb_minus_ne_dict(num2str(nb_minus_ne{i})) = obj.get_distance(nb_minus_ne{i});
            end
            keys = nb_minus_ne_dict.keys;
            values = nb_minus_ne_dict.values;
            [~, idx] = sort(cell2mat(values));
            keys = keys(idx);
        
            for i = 1:length(keys)
                route = str2num(keys{i});
                neighborhood = obj.neighborhood(route, obj.nrb);
                neighborhood_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
                for j = 1:length(neighborhood)
                    neighborhood_dict(num2str(neighborhood{j})) = obj.get_distance(neighborhood{j});
                end
                keys_neighborhood = neighborhood_dict.keys;
                values_neighborhood = neighborhood_dict.values;
                [~, idx_neighborhood] = sort(cell2mat(values_neighborhood));
                keys_neighborhood = keys_neighborhood(idx_neighborhood);
        
                obj.ns{i} = str2num(keys_neighborhood{1});
        
                if nb_minus_ne_dict(keys{i}) < obj.best_distance
                    obj.best_distance = nb_minus_ne_dict(keys{i});
                    obj.best_route = str2num(keys{i});
                    obj.ns{i} = str2num(keys_neighborhood{1});
                end
            end
        
            ns_route_dist_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(obj.ns)
                ns_route_dist_dict(num2str(obj.ns{i})) = obj.get_distance(obj.ns{i});
            end
            keys_ns = ns_route_dist_dict.keys;
            values_ns = ns_route_dist_dict.values;
            [~, idx_ns] = sort(cell2mat(values_ns));
            keys_ns = keys_ns(idx_ns);
            obj.ns = cellfun(@str2num, keys_ns, 'UniformOutput', false);
        end
        
        function global_search(obj)
            ns_minus_nb_random = arrayfun(@(x) obj.init_random_route(), 1:(obj.ns_int - obj.nb_int), 'UniformOutput', false);
        
            ns_minus_nb_random_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(ns_minus_nb_random)
                ns_minus_nb_random_dict(num2str(ns_minus_nb_random{i})) = obj.get_distance(ns_minus_nb_random{i});
            end
            keys = ns_minus_nb_random_dict.keys;
            values = ns_minus_nb_random_dict.values;
            [~, idx] = sort(cell2mat(values));
            keys = keys(idx);
        
            index = 1;
            for i = 1:length(keys)
                route = str2num(keys{i});
                dist = ns_minus_nb_random_dict(keys{i});
                if dist < obj.get_distance(obj.ns{index}) && ~any(cellfun(@(x) isequal(x, route), obj.ns))
                    obj.ns{index} = route;
        
                    if dist < obj.best_distance
                        obj.best_distance = dist;
                        obj.best_route = route;
                        obj.ns{index} = route;
                    end
                    index = index + 1;
                end
            end
        
            ns_route_dist_dict = containers.Map('KeyType', 'char', 'ValueType', 'double');
            for i = 1:length(obj.ns)
                ns_route_dist_dict(num2str(obj.ns{i})) = obj.get_distance(obj.ns{i});
            end
            keys_ns = ns_route_dist_dict.keys;
            values_ns = ns_route_dist_dict.values;
            [~, idx_ns] = sort(cell2mat(values_ns));
            keys_ns = keys_ns(idx_ns);
            obj.ns = cellfun(@str2num, keys_ns, 'UniformOutput', false);
        end
        
        function fit(obj, animate)
            distances = [];
            best_route_line = [];  % Initialize best_route_line here
        
            if animate
                fig = figure;
                axs(1) = subplot(1, 2, 1);
                axs(2) = subplot(1, 2, 2);
                best_route_line = animatedline(axs(2), 'Color', 'k', 'LineWidth', 2);
            end
        
            for iter = 1:obj.max_iter
                obj.best_search();  % best sites
                obj.elite_search();  % elite sites
                obj.global_search();  % global search
        
                distances = [distances, obj.best_distance];
                if animate
                    % Plot the best distance
                    plot(axs(1), 1:iter, distances);
                    xlabel(axs(1), 'Iteration');
                    ylabel(axs(1), 'Best Distance');
                    title(axs(1), sprintf('Best Distance over Iterations (%.2f)', obj.best_distance));
        
                    % Plot the best route
                    best_route_coords = obj.cities(obj.best_route, :);
                    if isvalid(best_route_line)
                        clearpoints(best_route_line);
                    end
                    if isvalid(best_route_line)
                        addpoints(best_route_line, best_route_coords(:, 1), best_route_coords(:, 2));
                    end
                    plot(axs(2), best_route_coords(:, 1), best_route_coords(:, 2), 'k-');
                    hold(axs(2), 'on');
                    scatter(axs(2), best_route_coords(:, 1), best_route_coords(:, 2), 100, 'red', 'filled');
                    hold(axs(2), 'off');
                    xlabel(axs(2), 'X');
                    ylabel(axs(2), 'Y');
                    title(axs(2), 'Best Route');
        
                    drawnow;
                    pause(0.01);
                elseif mod(iter, 50) == 0
                    fprintf('Best Distance: %.2f; Iteration: %d\n', obj.best_distance, iter);
                end
            end
        
            % Output the final best route
            fprintf('Best Route: %s\n', mat2str(obj.best_route));
            disp(['Best distance: ', num2str(obj.best_distance)]);
        end
    end
    
    end