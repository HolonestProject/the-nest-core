import numpy as np
import os
import pickle

# --- GENESIS PHYSICS CONSTANTS ---
DIMENSIONS = 1024  # The width of our holographic plate (Higher = clearer memories)
DENSITY = 0.1      # How "sparse" the vectors are (Biological neurons are sparse)

class HolographicEngine:
    def __init__(self):
        self.lexicon_path = os.path.expanduser("~/Genesis/nest_data/lexicon.pkl")
        self.lexicon = self._load_or_create_lexicon()

    def _load_or_create_lexicon(self):
        """
        The 'Alphabet of the Soul'.
        Assigns a random, immutable vector to every printable character.
        """
        if os.path.exists(self.lexicon_path):
            with open(self.lexicon_path, 'rb') as f:
                return pickle.load(f)
        else:
            print(" >> [PHYSICS] Forging new Lexicon...")
            lexicon = {}
            # Create vectors for ASCII chars (32-126)
            for i in range(32, 127):
                char = chr(i)
                # Sparse Random Projection
                vec = np.random.choice([0, 1], size=DIMENSIONS, p=[1-DENSITY, DENSITY])
                lexicon[char] = vec
            
            # Save it so 'A' is always 'A' forever.
            if not os.path.exists(os.path.dirname(self.lexicon_path)):
                os.makedirs(os.path.dirname(self.lexicon_path))
            with open(self.lexicon_path, 'wb') as f:
                pickle.dump(lexicon, f)
            return lexicon

    def text_to_hologram(self, text):
        """
        Transmutes Text -> Vector (Encoding).
        Uses 'Cyclic Shift' to preserve order (C-A-T is different from A-C-T).
        """
        if not text: return np.zeros(DIMENSIONS)
        
        hologram = np.zeros(DIMENSIONS)
        
        for index, char in enumerate(text):
            if char in self.lexicon:
                vec = self.lexicon[char]
                # Shift vector by position to encode sequence
                shifted_vec = np.roll(vec, index)
                # Superposition (Addition)
                hologram += shifted_vec
        
        # Binarize (Flatten back to 0/1 for storage efficiency)
        # This creates the 'Fingerprint'
        hologram = np.where(hologram > 0.5, 1, 0)
        return hologram

    def calculate_resonance(self, vec_a, vec_b):
        """
        Measures Similarity (Resonance).
        Returns 0.0 (No match) to 1.0 (Perfect match).
        """
        # Hamming Distance for binary vectors
        matches = np.sum(vec_a == vec_b)
        return matches / DIMENSIONS

    def bind_energy(self, content_vector, energy_level):
        """
        Applies 'Weight' (Arousal).
        Instead of changing the numbers, we scale the MAGNITUDE.
        """
        # For binary vectors, we can't scale magnitude directly in the array.
        # So we return a tuple: (Vector, Energy_Scalar)
        return (content_vector, energy_level)