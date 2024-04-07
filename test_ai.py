from ai.ai_logic import AILogic
from random import random

import time


if __name__ == "__main__":
    ai = AILogic()
    times = []
    for _ in range(100):
        test_set = [random() * 100 for _ in range(180)]
        start_time = time.time()
        result = ai.process(test_set)
        print(result)
        end_time = time.time()
        times.append(end_time - start_time)
    
    average_time = sum(times) / len(times)
    print(f"Took {average_time:.4f} seconds on average.")