from typing import List
from pynq import Overlay, allocate
import numpy as np

class AILogic:
    def __init__(self):
        overlay = Overlay("/home/xilinx/external_communication/ai/design_1.bit")
        self.dma = overlay.axi_dma_0
        self.input_buffer = allocate(shape=(36,), dtype=np.float32)
        self.output_buffer = allocate(shape=(1,), dtype=np.float32)
    
    def process(self, message: List[float]) -> str:
        ####################### Start of AI logic ########################
        ai_actions = ["ironMan", "hulk", "captAmerica", "shangChi", "bomb", "shield", "reload", "logout", "nothing"]
        for index, num in enumerate(message): self.input_buffer[index] = num
        
        try:
            self.dma.sendchannel.transfer(self.input_buffer)
            self.dma.recvchannel.transfer(self.output_buffer)
            self.dma.sendchannel.wait()
            self.dma.recvchannel.wait()
            result = ai_actions[int(self.output_buffer[0])]
        except Exception as e:
            print(f"ERROR is {e}")
            result = ai_actions[-1]
        print(f"THE RESULT IS {result}")
        ####################### End of AI logic ##########################
        return result