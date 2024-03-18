from multiprocessing import Process, Queue
from processes.grpc_server_process import grpc_server_process
from processes.mqtt_server_process import mqtt_server_process
from processes.evaluation_client_process import evaluation_client_process
from processes.mqtt_client_process import mqtt_client_process
from processes.game_engine_process import game_engine_process
from processes.grpc_client_process import grpc_client_process
from utils.logger import Logger

def get_user_input():
    """
    Gets user inputs

    Returns:
        list: Valid user inputs in the form of array
    """
    while True:
        try:
            port_num = int(input("Enter a port number: "))
            num_players = int(input("Enter the number of players: "))
            if num_players not in [1, 2]: raise Exception()
            does_not_have_visualiser = int(input("Enter 0 if there is no visualiser. Otherwise enter 1: ")) == 0
            return [port_num, num_players, does_not_have_visualiser]
        except:
            Logger.log("invalid input format")   

if __name__ == "__main__":
    #port_num, num_players, does_not_have_visualiser = get_user_input()
    port_num = 10000
    num_players = 1
    does_not_have_visualiser = True

    send_eval_server_game_state_queue = Queue()
    update_game_state_queue = Queue()
    outgoing_to_mqtt_queue = Queue()
    outgoing_queue_to_update_devices = Queue()
    incoming_from_mqtt_queue = Queue()
    grpc_client_queue = Queue()
    action_queue = Queue()

    # Spawn the processes
    p1 = Process(target=grpc_server_process, args=[action_queue])
    p2 = Process(target=mqtt_server_process, args=[action_queue, incoming_from_mqtt_queue])
    p3 = Process(target=evaluation_client_process, args=[send_eval_server_game_state_queue, update_game_state_queue, port_num])
    p4 = Process(target=mqtt_client_process, args=[outgoing_to_mqtt_queue])
    p5 = Process(target=game_engine_process, args=[
        action_queue, 
        incoming_from_mqtt_queue, 
        outgoing_to_mqtt_queue,
        send_eval_server_game_state_queue,
        update_game_state_queue,
        num_players,
        does_not_have_visualiser,
        grpc_client_queue
    ])
    p6 = Process(target=grpc_client_process, args=[grpc_client_queue])
    processes = [p1, p2, p3, p4, p5, p6]
    for p in processes: p.start()
    for p in processes: p.join()
