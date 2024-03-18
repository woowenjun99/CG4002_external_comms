from api.evaluation_client import EvaluationClient
from multiprocessing import Queue
from utils.logger import Logger

def evaluation_client_process(
    send_eval_server_game_state_queue: Queue,
    update_game_state_queue: Queue,
    port_num: int
):
    """
    This process is used to keep the websocket connection alive,
    send and receive message from the evaluation server
    """
    client = EvaluationClient(port_num)
    client.establish_handshake()

    # Required to keep the socket running. Otherwise connection will close.
    while True:
        predicted_game_state: str = send_eval_server_game_state_queue.get()
        Logger.log(f"The predicted game state is {predicted_game_state}")
        client.send_message(predicted_game_state)
        updated_game_state_str = client.receive_message()
        update_game_state_queue.put(updated_game_state_str)