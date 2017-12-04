max_depth = 3
possible_tile_values = [2, 4]
evaluated = 0

evaluation_matrix = [[7,5,4,3],\
                     [5,4,3,2],\
                     [4,3,2,1],\
                     [3,2,1,0]]

def minimax(game_state):
    global evaluated
    moves = game_state.getAvailableMoves()
    best_move = moves[0]
    best_score = float('-inf')
    evaluated += 1
    for move in moves:
        clone = game_state.clone()
        clone.move(move)
        score = max_play(clone, 0, float('-inf'), float('inf'))
        if score > best_score:
            best_move = move
            best_score = score
    print(evaluated)
    evaluated = 0
    return best_move

def min_play(game_state, depth, alpha, beta):
    global evaluated
    if depth >= max_depth:
        return evaluate(game_state)
    cells = game_state.getAvailableCells()
    min_score = float('inf')
    depth += 1
    evaluated += 1
    done = False
    for cell in cells:
        if done:
            break
        for value in possible_tile_values:
            clone = game_state.clone()
            clone.insertTile(cell, value)
            score = max_play(clone, depth, alpha, beta)
            if score < min_score:
                min_score = score
            if min_score <= alpha:
                done = True
                break
            if min_score < beta:
                beta = min_score

    return min_score

def max_play(game_state, depth, alpha, beta):
    global evaluated
    if depth >= max_depth:
        return evaluate(game_state)
    moves = game_state.getAvailableMoves()
    max_score = float('-inf')
    depth += 1
    evaluated += 1
    for move in moves:
        clone = game_state.clone()
        clone.move(move)
        score = min_play(clone, depth, alpha, beta)
        if score > max_score:
            max_score = score
        if max_score >= beta:
            break
        if max_score > alpha:
            alpha = max_score
    return max_score

def evaluate(grid):
    '''
    max_tile = 0
    tile_sum = 0
    empty_tiles = 0

    for x in range(grid.size):
        for y in range(grid.size):
            max_tile = max(max_tile, grid.map[x][y])
            empty_tiles += 0 if grid.map[x][y] else 1
            tile_sum += grid.map[x][y]

    return max_tile + tile_sum - 2**(int(abs(grid.size * grid.size - empty_tiles)))
    '''
    monotonicity_score = 0
    smoothness_score = 0
    mergable = 0
    for x in range(grid.size):
        for y in range(grid.size):
            monotonicity_score += evaluation_matrix[x][y] * grid.map[x][y]
            if x + 1 < grid.size:
                if grid.map[x + 1][y] == grid.map[x][y]:
                    mergable += 1
            if y + 1 < grid.size:
                if grid.map[x][y + 1] == grid.map[x][y]:
                    mergable += 1

    return monotonicity_score + mergable**4


