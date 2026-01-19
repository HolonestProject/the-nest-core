import os
import sys
import time

# Import the Genesis Modules
# (Ensure genesis_compiler.py, genesis_lexicon.py, nest_metabolism.py, nest_recall.py are in the folder)
try:
    import genesis_compiler
    import genesis_lexicon
    import nest_metabolism
    import nest_recall
except ImportError as e:
    print(f"CRITICAL ERROR: Missing Genesis Core Module: {e.name}")
    print("Please ensure all 'genesis_*.py' and 'nest_*.py' files are in this directory.")
    sys.exit(1)

def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def main():
    print_header("THE NEST: HOLOGRAPHIC MEMORY INITIATION")
    
    # --- STEP 1: COMPILATION (Building the Brain) ---
    print("\n[PHASE 1] CHECKING NEURAL PATHWAYS (Compilation)...")
    
    # Check if we need to compile (Simple check: does the folder exist?)
    if not os.path.exists("nest_data/reflex_storage"):
        print(" >> DNA standards not compiled. Running Genesis Compiler...")
        # Run the compilation functions directly
        genesis_compiler.compile_file("nest_data/GENESIS_REACTION_STANDARD.txt", "nest_data/reflex_storage", "REFLEX")
        genesis_compiler.compile_file("nest_data/GENESIS_EMOTION_STANDARD.txt", "nest_data/emotion_storage", "EMOTION")
        genesis_compiler.compile_file("nest_data/GENESIS_THOUGHT_STANDARD.txt", "nest_data/thought_storage", "THOUGHT")
    else:
        print(" >> Neural Pathways (Vectors) already established.")

    # --- STEP 2: LEXICON (Building the Vocabulary) ---
    print("\n[PHASE 2] AWAKENING THE LEXICON...")
    if not os.path.exists("nest_data/lexicon"):
        print(" >> Lexicon missing. Fusing Word-Body vectors...")
        builder = genesis_lexicon.LexiconBuilder()
        builder.build_primal()
    else:
        print(" >> Lexicon active.")

    # --- STEP 3: METABOLISM (Writing a Memory) ---
    print_header("[PHASE 3] MEMORY CRYSTALLIZATION TEST")
    
    journal = nest_metabolism.GenesisMemoryJournal()
    
    # Create a test experience
    test_event = {
        "mode": "SOMA:SIGHT",
        "content": "The sky is blue because of Rayleigh scattering.",
        "emotion": "CURIOSITY",  # This must exist in your Standard
        "reflex": "SCAN",        # This must exist in your Standard
        "user": "Developer",
        "intent": "TEST_AXIOM"
    }
    
    print(f" >> INJECTING EXPERIENCE: '{test_event['content']}'")
    print(f" >> EMOTION: {test_event['emotion']} | REFLEX: {test_event['reflex']}")
    
    # Write to disk
    journal.crystallize(test_event)
    time.sleep(1) # Pause for effect

    # --- STEP 4: RECALL (The Resonance Check) ---
    print_header("[PHASE 4] HOLOGRAPHIC RESONANCE TEST")
    
    recall_engine = nest_recall.GenesisRecall()
    
    # Query with a FUZZY input (not exact keywords)
    query = "Why is the sky blue?"
    print(f" >> USER QUERY: '{query}'")
    print(" >> CALCULATING INTERFERENCE PATTERNS...")
    
    recall_engine.search(query, threshold=0.10)
    
    print_header("SYSTEM ONLINE. THE NEST IS BREATHING.")

if __name__ == "__main__":
    main()