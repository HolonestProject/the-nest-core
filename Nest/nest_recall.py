import os
import glob
import numpy as np
import nest_holography 

class GenesisRecall:
    def __init__(self):
        self.physics = nest_holography.HolographicEngine()
        
    def search(self, query, search_locations, threshold=0.1):
        """
        The Act of Remembering.
        ARGS:
            query (str): What to look for.
            search_locations (list): A list of folder paths to scan.
        """
        print(f" >> [MNEMOSYNE] Scanning specific sectors: {[os.path.basename(p) for p in search_locations]}...")
        
        # 1. Transmute Query to Vector
        query_vec = self.physics.text_to_hologram(query)
        
        results = []
        
        # 2. Iterate ONLY through the requested locations
        for folder in search_locations:
            if not os.path.exists(folder):
                continue
                
            memories = glob.glob(os.path.join(folder, "*.npy"))
            
            for mem_file in memories:
                try:
                    data = np.load(mem_file, allow_pickle=True).item()
                    stored_vec = data['hologram']
                    
                    resonance = self.physics.calculate_resonance(query_vec, stored_vec)
                    
                    if resonance > threshold:
                        results.append((resonance, data))
                except:
                    continue
        
        # 3. Sort
        results.sort(key=lambda x: x[0], reverse=True)
        
        # 4. Report
        if not results:
            print(" >> [MNEMOSYNE] No resonance found in these sectors.")
        else:
            top = results[0]
            print(f" >> [MNEMOSYNE] Match ({top[0]:.2f}): '{top[1]['raw_content']}'")
            
        return results