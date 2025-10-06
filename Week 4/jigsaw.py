% Load scrambled image
load('scrambled_lena.mat');   % loads Iscrambled
I = double(Iscrambled);

% Puzzle parameters
N = 8;                         % number of tiles per row/column (8x8 = 64 pieces)
tileSize = size(I,1) / N;

% Divide image into tiles
tiles = mat2cell(I, tileSize*ones(1,N), tileSize*ones(1,N));

% Start from a random arrangement
perm = randperm(N*N);
current_state = reshape(perm, [N, N]);

% --- Energy (cost) function ---
function E = energy(tiles, state)
  N = size(state,1);
  E = 0;
  for i = 1:N
    for j = 1:N
      tile = tiles{state(i,j)};
      % Compare right edge
      if j < N
        right_tile = tiles{state(i,j+1)};
        E = E + sum((tile(:,end) - right_tile(:,1)).^2);
      end
      % Compare bottom edge
      if i < N
        bottom_tile = tiles{state(i+1,j)};
        E = E + sum((tile(end,:) - bottom_tile(1,:)).^2);
      end
    end
  end
end

% --- Simulated Annealing Parameters ---
T = 10000;           % initial temperature
T_min = 1e-3;
alpha = 0.99;
E_curr = energy(tiles, current_state);
best_state = current_state;
best_E = E_curr;

% --- Simulated Annealing Loop ---
while T > T_min
  for iter = 1:100
    new_state = current_state;
    idx = randperm(numel(new_state), 2);
    % Swap two tiles
    tmp = new_state(idx(1));
    new_state(idx(1)) = new_state(idx(2));
    new_state(idx(2)) = tmp;
    
    E_new = energy(tiles, new_state);
    dE = E_new - E_curr;

    % Accept or reject
    if dE < 0 || rand() < exp(-dE/T)
      current_state = new_state;
      E_curr = E_new;
      if E_curr < best_E
        best_state = current_state;
        best_E = E_curr;
      end
    end
  end
  T = T * alpha;  % cool down
  fprintf('Temp: %.3f | Best Energy: %.3f\n', T, best_E);
end

% --- Reconstruct image from best state ---
final_tiles = tiles(best_state(:));
I_reconstructed = cell2mat(reshape(final_tiles, [N, N]));

% --- Display results ---
figure;
subplot(1,2,1); imshow(uint8(I)); title('Scrambled Image');
subplot(1,2,2); imshow(uint8(I_reconstructed)); title('Reconstructed Image');
