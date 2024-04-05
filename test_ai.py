from ai.ai_logic import AILogic
from random import random

if __name__ == "__main__":
    ai = AILogic()
    for _ in range(5):
        test_set = [[(random() * 100) for _ in range(6)] for _ in range(30)]
        result = ai.process(test_set)
        print(result)