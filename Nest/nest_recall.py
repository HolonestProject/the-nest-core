import os
import json
import numpy as np
from datetime import datetime

# --- CONFIG ---
NEST_PATH = "nest_data"
HOT_PATH = os.path.join(NEST_PATH, "hot_quits")
QUIT_DIMENSION = 1024

class HolographicReader:
    def __init__(self):
        print(f"[{datetime.now()}] READER: Scanning Holographic Field...")
        
        # Load all memories into RAM for the demo
        # (In a real production system, we would stream this)
        self.memories = []
        self._load_memory_bank()

    def _text_to_quits(self, text):
        """
        Replicates the Encoder logic to ensure the Query speaks the same language
        as the Memories.
        """
        seed = hash(text) % (2**32)
        rng = np.random.default_rng(seed)
        dna_bases = rng.integers(0, 4, QUIT_DIMENSION)
        phases = dna_bases * (np.pi / 2)
        return np.exp(1j * phases)

    def _load_memory_bank(self):
        """
        Loads every .npy crystal from the Hot Folder.
        """
        if not os.path.exists(HOT_PATH):
            print("WARNING: No memories found. Ingest something first.")
            return

        files = [f for f in os.listdir(HOT_PATH) if f.endswith('.npy')]
        print(f"Found {len(files)} memory crystals.")

        for f in files:
            file_path = os.path.join(HOT_PATH, f)
            meta_path = file_path.replace('.npy', '.meta.json')
            
            # Load the Wave
            wave = np.load(file_path)
            
            # Load the Text (so we can show the human what we found)
            try:
                with open(meta_path, 'r') as json_file:
                    meta = json.load(json_file)
            except:
                meta = {"content": "UNKNOWN DATA"}

            self.memories.append({
                "filename": f,
                "wave": wave,
                "meta": meta
            })

    def search(self, query_text):
        """
        The Core Tech: Phase Coherence Check.
        Compares the Query Wave vs. Memory Waves.
        """
        print(f"\n--- QUERY: '{query_text}' ---")
        
        # 1. Convert Query to Wave
        query_wave = self._text_to_quits(query_text)
        
        results = []
        
        for mem in self.memories:
            # 2. Resonance Calculation (Dot Product)
            # This measures how much the two waves overlap in 1024 dimensions.
            # We use the absolute value of the dot product as the "Score".
            resonance = np.abs(np.vdot(query_wave, mem["wave"]))
            
            # Normalize score (0 to 1 scale roughly) for display
            score = resonance / QUIT_DIMENSION
            
            results.append((score, mem))

        # 3. Sort by highest resonance
        results.sort(key=lambda x: x[0], reverse=True)

        # 4. Display Top Match
        if results:
            top_score, top_mem = results[0]
            print(f"TOP MATCH (Resonance: {top_score:.4f})")
            print(f"File: {top_mem['filename']}")
            print(f"Content: \"{top_mem['meta']['content']}\"")
        else:
            print("No resonance found.")

if __name__ == "__main__":
    reader = HolographicReader()
    
    # DEMO: Ask the user for a query
    user_query = input("\nEnter search term: ")
    reader.search(user_query)