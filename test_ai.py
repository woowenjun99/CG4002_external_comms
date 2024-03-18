from ai.ai_logic import AILogic
from random import randint

if __name__ == "__main__":
    ai = AILogic()
    for _ in range(5):
        test_set = [[randint(1, 6) for _ in range(6)] for _ in range(100)]
        result = ai.process(test_set)
        print(result)