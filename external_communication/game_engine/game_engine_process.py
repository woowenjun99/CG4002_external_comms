from external_communication.game_engine.GameEngine import GameEngine
from multiprocessing import Queue
from json import dumps, loads
from time import time

def game_engine_process(
        action_queue: Queue,
        incoming_from_mqtt_queue: Queue, 
        outgoing_to_mqtt_queue: Queue,
        send_eval_server_game_state_queue: Queue,
        update_game_state_queue: Queue,
        num_players: int,
        does_not_have_visualiser,
        grpc_client_queue: Queue
):
    # Initialise game engine and send the initial values over
    game_engine = GameEngine(num_players, does_not_have_visualiser)

    while True:
        message = loads(action_queue.get())
        action = message["action"]
        player_id = message["player_id"]

        is_in_vision = True
        if action != "oppStepIntoBomb" and action != "logout":
            try: 
                outgoing_to_mqtt_queue.put(dumps({
                    "topic": f"to_visualiser/visibility/p{player_id}",
                    "player_id": player_id, 
                    "request_data": True,
                    "timestamp": time()
                }))
                # NOTE Need to check if player_id == received_message.player_id
                received_message = incoming_from_mqtt_queue.get(timeout=2)
                is_in_vision = loads(received_message)["opponent_in_view"]
            except: is_in_vision = False

        status = game_engine.perform_action(action, player_id, is_in_vision)
        predicted_game_state = game_engine.game_state.get_dict()

        # Update the game state logic by getting the correct game state from evaluation server
        # we dont update eval server if its oppstepintobomb
        if action != "oppStepIntoBomb":
            try:
                send_eval_server_game_state_queue.put(dumps({
                    "action": action,
                    "game_state": predicted_game_state,
                    "player_id": 1 if player_id == 2 else 1
                }))
                correct_game_state = loads(update_game_state_queue.get(timeout=2))
            except: correct_game_state = predicted_game_state.copy()

        # Update the game state locally
        game_engine.game_state.set_state(correct_game_state)

        # Update the game state in 2 other processes
        outgoing_to_mqtt_queue.put(dumps({
            "topic": "to_visualiser/gamestate/",
            "game_state": {
                "p1": correct_game_state["p1"],
                "p2": correct_game_state["p2"]
            },
            "player_id": player_id,
            "action": action,
            "status": status,
            "timestamp": time()
        }))

        grpc_client_queue.put(dumps({
            "p1": correct_game_state["p1"],
            "p2": correct_game_state["p2"]
        }))
