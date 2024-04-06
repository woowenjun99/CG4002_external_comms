from external_communication.game_engine.GameEngine import GameEngine
from multiprocessing import Queue
from json import dumps, loads
from time import time

def game_engine_process(
    action_queue_1: Queue,
    action_queue_2: Queue,
    incoming_from_mqtt_queue: Queue, 
    outgoing_to_mqtt_queue: Queue,
    send_eval_server_game_state_queue: Queue,
    update_game_state_queue: Queue,
    num_players: int,
    does_not_have_visualiser,
    grpc_client_queue: Queue,
    player_turn
):
    # Initialise game engine and send the initial values over
    game_engine = GameEngine(num_players, does_not_have_visualiser)
    action_not_requiring_visibility_check = ["oppStepIntoBomb", "logout"]
    action_not_requiring_update_to_eval_server = ["oppStepIntoBomb"]
  

    while True:
        if player_turn.value == 1:
            message = loads(action_queue_1.get())
            print("TOP1" + message["action"])

        elif player_turn.value == 2:
            message = loads(action_queue_2.get())
            print("TOP2" + message["action"])

            
        action = message["action"]
        player_id = message["player_id"]
        timestamp = time()
        
        # If there is no action, we just inform the MQTT
        if action == "nothing":
            predicted_game_state = game_engine.game_state.get_dict()
            outgoing_to_mqtt_queue.put(dumps({
                "topic": "to_visualiser/gamestate/",
                "action": action,
                "game_state": {
                    "p1": predicted_game_state["p1"],
                    "p2": predicted_game_state["p2"]
                },
                "player_id": player_id,
                "status": "Please Redo!",
                "timestamp": timestamp
            }))
            continue

        is_in_vision = True
        number_of_fire = 0
        if action not in action_not_requiring_visibility_check:
            # check for visibility
            try: 
                outgoing_to_mqtt_queue.put(dumps({
                    "topic": f"to_visualiser/visibility/p{player_id}",
                    "player_id": player_id, 
                    "request_data": True,
                    "timestamp": timestamp
                }))
                # NOTE Need to check if player_id == received_message.player_id
                received_message = incoming_from_mqtt_queue.get(timeout=2)
                print(received_message)
                is_in_vision = loads(received_message)["opponent_in_view"]
                number_of_fire = loads(received_message)["number_of_fire"]
            except: 
                is_in_vision = True
                number_of_fire = 0

        if (number_of_fire > 0):
            for _ in range(number_of_fire):
                game_engine.perform_action("oppStepIntoBomb", player_id, True)

        status = game_engine.perform_action(action, player_id, is_in_vision)
        predicted_game_state = game_engine.game_state.get_dict()

        # Update the game state logic by getting the correct game state from evaluation server
        # we dont update eval server if its oppstepintobomb
        if action not in action_not_requiring_update_to_eval_server:
            try:
                send_eval_server_game_state_queue.put(dumps({
                    "action": action,
                    "game_state": predicted_game_state,
                    "player_id": player_id
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
            "timestamp": timestamp
        }))

        grpc_client_queue.put(dumps({
            "p1": correct_game_state["p1"],
            "p2": correct_game_state["p2"]
        }))

        # now we switch the player turn
        player_turn.value = 2 if player_turn.value == 1 else 1
        
        # we are at the next stage, we flush 
        if player_turn.value == 1:
            # player_turn 3 means blocked
            player_turn.value = 3
            action_queue_1.put(dumps({
                "action": "CHECKPOINT",
                "player_id": 1
            }))

            print("Adding checkpoint for player 1")

            action_queue_2.put(dumps({
                "action": "CHECKPOINT",
                "player_id": 2
            }))
            print("Adding checkpoint for player 2")


            while not action_queue_1.empty(): 
                print("Current for p1")
                print(current)
                current = loads(action_queue_1.get())
                if current["action"] == "CHECKPOINT": 
                    print("Checkpoint reached for player 1")
                    break

            
            while not action_queue_2.empty(): 
                current = loads(action_queue_2.get())
                print("Current for p2")
                print(current)
                if current["action"] == "CHECKPOINT": 
                    print("Checkpoint reached for player 2")
                    break

            player_turn.value = 1




