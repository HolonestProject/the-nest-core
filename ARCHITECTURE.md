# The Nest: Holographic Phase-Space Memory Engine

> "Conventional AI records data in rows. The Nest records data in interference patterns."

## 1. The Core Philosophy
The Nest is a **Vector Symbolic Architecture (VSA)** library designed to solve the "Catastrophic Forgetting" problem in modern AI. It provides a persistent, dynamic memory layer based on **Quit Logic (Phase Space)**, treating data as complex phasors on the unit circle.

### Why Phase Space?
In binary logic, adding data increases size. In Phase Space ($1 \angle 0^\circ + 1 \angle 180^\circ = 0$), adding data creates **interference**. 
* **Infinite Superposition:** Stack thousands of memories into a single 1024-dimensional vector.
* **Natural Filtering:** Random noise cancels out; repeated patterns (wisdom) amplify through constructive interference.

## 2. The Physics Engine (`nest_holography.py`)
The core engine operates on **Complex128** arrays with a fixed dimension of **1024**.

### The Math
Every concept is mapped to a vector $z$ where:
$$z = e^{i\theta}$$

### Core Operations
* **Binding (Multiplication):** $A \otimes B$. Attaches attributes (e.g., "Color" to "Object").
* **Bundling (Addition):** $A + B$. Fuses multiple memories into a single holographic slot.
* **Resonance (Dot Product):** $|A \cdot B|$. Measures similarity for recall.

## 3. The Trinity Anchors (The DNA)
The Nest is seeded with immutable **Phase Anchors**—fixed vectors that act as the system's "Initial Values" and reference frame.

* **Reflex (Survival):** High-energy patterns like the **JOLT** vector for hardware-level interrupts.
* **Emotion (Gravity):** A coordinate system (Valence/Arousal) used to calculate **Mass**. High-mass memories sink into long-term storage.
* **Thought (Authentication):** Phase-rotation keys used to tag the source of a memory.
    * **SOMA Channel:** $0^\circ$ rotation for empirical sensor data.
    * **PNEUMA Channel:** $90^\circ$ ($i$) rotation for trusted/injected truths.

## 4. Storage & Retrieval Flow

### Crystallization (Write)
Handled by `nest_metabolism.py`. It does not "see" or "process" raw images; it only "crystallizes" what the user provides.
1.  **Input:** Accepts raw Text or **Pre-processed Vectors** (e.g., 1024-dim visual vectors).
2.  **Fusion:** If text, transmutes to Phase. If Vector, validates dimensions.
3.  **DNA Injection:** Mathematically adds the specified **Reflex** and **Emotion** vectors to the content.
4.  **Storage:** Writes the final `.npy` crystal to the commanded location.

### Resonance (Read)
Handled by `nest_recall.py`.
1.  **Scan:** Dot-products a query vector against crystals in specified sectors.
2.  **Match:** Returns memories where Resonance $> 0.15$.

## 5. System Topology
The Nest is a **Dumb and Obedient** tool. It contains no decision logic regarding *what* to remember or *how* to see.

```mermaid
graph TD
    User[Queen / Client Logic] --> |"Command: SAVE Vector/Text"| Scribe[nest_metabolism.py]
    User --> |"Command: SEARCH query"| Mnemosyne[nest_recall.py]
    
    subgraph "The Nest Library"
        Physics[nest_holography.py]
        Lexicon[Phase Lexicon]
    end
    
    Scribe --> Physics
    Mnemosyne --> Physics
    
    Physics --> |Phase Vector| Disk[(.npy Storage)]