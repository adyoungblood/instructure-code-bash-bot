import requests
import copy

base_url = 'http://light-bikes.inseng.net/games'
timeout = 3

def index():
    return requests.get(base_url, timeout = timeout)

def create(add_server_bot = None, board_size = None, num_players = None, server_bot_difficulty = None):
    return requests.post(base_url, params={
        'addServerBot': add_server_bot,
        'boardSize': board_size,
        'numPlayers': num_players,
        'serverBotDifficulty': server_bot_difficulty
    }, timeout = timeout)

def show(game_id):
    return requests.get('{0}/{1}'.format(base_url, game_id), timeout = timeout)

def join_game(game_id, name):
    return requests.post('{0}/{1}/join'.format(base_url, game_id), params={
        'name': name,
    }, timeout = timeout)

def move(game_id, player_id, x, y):
    return requests.post('{0}/{1}/move'.format(base_url, game_id), params={
        'playerId': player_id,
        'x': x,
        'y': y
    }, timeout = timeout)

# -----------------

sight = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0]
]

def get_next_position(current_x, current_y, board, max_depth = 2, depth = 0):
    if depth > max_depth:
        return

    potential_next_positions = []
    for offset in sight:
        new_x = current_x + offset[0]
        new_y = current_y + offset[1]
        # stuff = (len(board), len(board[0]), board[new_x][new_y])
        if new_x >= 0 and new_y >= 0 and new_x < len(board) and new_y < len(board[0]) and board[new_x][new_y] == None:
            simulated_board = copy.deepcopy(board)
            simulated_board[new_x][new_y] = 'bleh'
            next_next_position = get_next_position(new_x, new_y, simulated_board, max_depth, depth + 1)
            if next_next_position != (new_x, new_y):
                potential_next_positions.append((new_x, new_y))

    if len(potential_next_positions) == 0:
        return (current_x, current_y)

    potential_next_position = potential_next_positions[0]
    potential_next_sticky_positions = []
    if depth == 0:
        for position in potential_next_positions:
            can_stick = False
            for offset in sight:
                new_x = position[0] + offset[0]
                new_y = position[1] + offset[1]
                if new_x >= 0 and new_y >= 0 and new_x < len(board) and new_y < len(board[0]) and board[new_x][new_y] is not None:
                    can_stick = True
                    break
            if can_stick:
                potential_next_sticky_positions.append(position)
        potential_next_sticky_positions
    return potential_next_sticky_positions[0] if len(potential_next_sticky_positions) > 0 else potential_next_position

# -----------------

def main(max_depth):
    should_create = True if input('Create a new game? (y)/n') == '' else False
    if should_create: 
        game_id = create(add_server_bot = True, server_bot_difficulty = 4).json()['id']
    else:
        game_id = int(input('Input game ID: '))
    response = join_game(game_id, 'Alexander')
    game_state = response.json()[0]
    player_id = game_state['current_player']['id']
    player_color = game_state['current_player']['color']
    status_code = response.status_code
    # print(game_state)
    while status_code == 200:
        game_state = response.json()[0]
        current_x = game_state['current_player']['x']
        current_y = game_state['current_player']['y']
        board = game_state['board']
        next_move = get_next_position(current_x, current_y, board, max_depth)
        response = move(game_id, player_id, next_move[0], next_move[1])
        status_code = response.status_code
        # print(response.status_code, response.json())
    final_game_state = show(game_id).json()
    if final_game_state['games'][0]['winner'] == player_color:
        print('You won!')
    else:
        print('You lost...')
def test(max_depth):
    test_board = [
        [1, 1, None, None, None],
        [1, None, None, None, None],
        [None, None, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    print(get_next_position(2, 2, test_board, max_depth))

if __name__ == '__main__':
    main(2)
    
