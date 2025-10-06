% N  - number of nodes
% D  - distance matrix
% s  - current tour
% p  - transition probability
% d  - tour cost per iteration

clear all; close all; clc;
rng(100);   % for reproducibility

% -------- Generate random nodes in 2D plane -------------
N = 30;                          % number of cities (use 1000 for large test)
x = rand(2, N);                  % random coordinates
D = zeros(N, N);                 % distance matrix

for i = 1:N-1
    for j = i+1:N
        D(i,j) = norm(x(:,i) - x(:,j));  % Euclidean distance
        D(j,i) = D(i,j);
    end
end
% ---------------------------------------------------------

% ---- Initialization -------------------------------------
s = randperm(N);                 % initial random tour
s_init = s;
ds = path_cost_tour(s, D);       % initial cost
d = ds;                          % store cost evolution
p = [];                          % store acceptance probabilities

Tm = 1000;                       % initial temperature
iter_max = 500000;               % max iterations
% ---------------------------------------------------------

% ---------------- Simulated Annealing ---------------------
for i = 1:iter_max
    % Generate neighbor (2-opt swap)
    id = sort(randperm(N, 2));
    s_next = s;
    s_next(id(1):id(2)) = s(id(2):-1:id(1));

    % Compute cost difference
    ds_next = path_cost_tour(s_next, D);
    E = ds - ds_next;            % energy difference
    T = Tm / i;                  % temperature schedule
    pE = 1 / (1 + exp(-E / T));  % acceptance probability

    % Accept or reject the move
    if E > 0
        s = s_next;
    elseif rand < pE
        s = s_next;
    end

    % Update values
    ds = path_cost_tour(s, D);
    d = [d, ds];
    p = [p, pE];
end
% ---------------------------------------------------------

% ---------------- Plot Results ----------------------------
figure;
subplot(1,2,1);
axis([0 1 0 1]);
plot(x(1,[s_init s_init(1)]), x(2,[s_init s_init(1)]), '-o');
title('Initial Random Tour');

subplot(1,2,2);
axis([0 1 0 1]);
plot(x(1,[s s(1)]), x(2,[s s(1)]), '-o');
title('Optimized Tour (Simulated Annealing)');
% ---------------------------------------------------------

% ---------------- Helper Function -------------------------
function cost = path_cost_tour(s, D)
    cost = 0;
    for i = 1:length(s)-1
        cost = cost + D(s(i), s(i+1));
    end
    cost = cost + D(s(end), s(1));   % return to start
end
% ---------------------------------------------------------
