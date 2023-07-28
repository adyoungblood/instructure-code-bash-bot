import requests

base_url = 'http://light-bikes.inseng.net/games'

def create_query_string(**kwargs):
    query_string = ''
    for key, value in kwargs.items():
        if value is not None:
            query_string += '{0}={1}&'.format(key, value)
    return query_string

def index():
    return requests.get(base_url)

def create(add_server_bot = None, board_size = None, num_players = None, server_bot_difficulty = None):
    return requests.post(base_url, params={
        'addServerBot': add_server_bot,
        'boardSize': board_size,
        'numPlayers': num_players,
        'serverBotDifficulty': server_bot_difficulty
    })

def show(game_id):
    return requests.get('{0}/{1}'.format(base_url, game_id))

def join_game(game_id, name):
    return requests.post('{0}/{1}/join'.format(base_url, game_id), params={
        'name': name,
    })

def move(game_id, player_id, x, y):
    return requests.post('{0}/{1}/move'.format(base_url, game_id), params={
        'playerId': player_id,
        'x': x,
        'y': y
    })

# -----------------

sight = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1]
]

def next_position(current_x, current_y, board):
    for offset in sight:
        new_x = current_x + offset[0]
        new_y = current_y + offset[1]
        if new_x >= 0 and new_y >= 0 and new_x < len(board) and new_y < len(board[0]) and board[new_x][new_y] == None:
            return (new_x, new_y)
    return (current_x, current_y)

# -----------------

if __name__ == '__main__':
    game_id = create(add_server_bot = True, server_bot_difficulty = 3).json()['id']
    response = join_game(game_id, 'Alexander')
    game_state = response.json()[0]
    player_id = game_state['current_player']['id']
    status_code = response.status_code
    while status_code == 200:
        game_state = response.json()[0]
        current_x = game_state['current_player']['x']
        current_y = game_state['current_player']['y']
        board = game_state['board']
        next_move = next_position(current_x, current_y, board)
        response = move(game_id, player_id, next_move[0], next_move[1])
        status_code = response.status_code
        print(response.status_code, response.json())
    
