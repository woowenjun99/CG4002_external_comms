from typing import List
from scipy.stats import median_absolute_deviation, iqr
from pynq import Overlay, allocate
import numpy as np
import statistics
from sklearn.preprocessing import MinMaxScaler

class AILogic:
    def __init__(self):
        overlay = Overlay("/home/xilinx/external_comms/ai/design_1.bit")
        self.dma = overlay.axi_dma_0
        self.input_buffer = allocate(shape=(36,), dtype=np.float32)
        self.output_buffer = allocate(shape=(1,), dtype=np.float32)
    
    def process(self, message: List[List[float]]) -> str:
        ####################### Start of AI logic ########################
        ai_actions = ["ironMan", "hulk", "captAmerica", "shangChi", "bomb", "shield", "reload", "logout", "nothing"]
        
        # Normalise the data
        scaler = MinMaxScaler()
        scaler.fit(message)
        normalised_new_data = scaler.transform(message)
        npx = np.array(normalised_new_data)
        input_buffer = []
        for i in range(6):
            vals = npx[:,i]
            mean = statistics.mean(vals)
            mad = median_absolute_deviation(vals)
            std = statistics.stdev(vals)
            inqr = iqr(vals)
            max = np.max(vals)
            min = np.min(vals)
            col = [mean, mad, std, inqr, max, min]
            input_buffer.extend(col)
        
        self.input_buffer = input_buffer
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
        # result = ai_actions[randint(0, len(ai_actions) - 1)]
        ####################### End of AI logic ##########################
        return result