## **Understanding the Encoding Mechanism**
Each chess game in the provided PGN file contains:
- A sequence of moves.
- A "Trailing" header specifying the number of bits to ignore.
- The position of a move within the list of legal moves determines the extracted bits.

### **Encoding Breakdown**
1. Each legal move has an index within `board.legal_moves`.
2. The number of legal moves determines how many bits can be extracted (`floor(log2(no_moves))`).
3. The "Trailing" value tells us how many bits to ignore.
4. The final binary sequence is constructed from relevant move indices.

---

## **Solution Approach**
### **Step 1: Parsing the PGN File**
The script reads each chess game from the PGN file and initializes a chess board.

### **Step 2: Extracting Bits**
- For each move, it computes the move index within `legal_moves`.
- Converts this index into a binary string.
- Extracts the significant bits (removing trailing bits if needed).
- Collects these bits to form the flag in binary.

### **Step 3: Converting Binary to Bytes**
- The binary bitstream is grouped into bytes (8 bits each).
- Each byte is converted into a character.

### **Step 4: Decoding the Flag**
- The extracted byte sequence is attempted to be decoded using common encodings (`ascii`, `utf-8`, `latin1`, `cp1252`).
- A hexadecimal representation of the byte sequence is also printed for further analysis.

---

## **Python Solution**
```python
import chess
import chess.pgn
from math import floor, log2
import io

def decrypt_flag(pgn_filename):
    pgn_file = open(pgn_filename)
    flag_bits = []
    game_count = 0
    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None: 
            break
        game_count += 1
        print(f"Processing game {game_count}")
        board = chess.Board()
        trailing = int(game.headers.get('Trailing', '0'))
        print(f"Trailing bits: {trailing}")
        move_count = 0
        for move in game.mainline_moves():
            move_count += 1
            legal_moves = list(board.legal_moves)
            no_moves = len(legal_moves)
            log2_len = floor(log2(no_moves))
            
            # Find the move index
            move_index = legal_moves.index(move)
            print(f"Move {move_count}: {move}, Index: {move_index}, Legal moves: {no_moves}")
            
            # Convert move index to binary and get relevant bits
            binary = format(move_index, f'0{log2_len}b')
            chunk_size = log2_len - trailing
            relevant_bits = binary[:chunk_size]
            print(f"Binary: {binary}, Chunk size: {chunk_size}, Relevant bits: {relevant_bits}")
            flag_bits.extend(int(bit) for bit in relevant_bits)

            board.push(move)
        trailing = 0
    print(f"\nTotal bits collected: {len(flag_bits)}")
    print(f"First 50 bits: {''.join(str(bit) for bit in flag_bits[:50])}")
    flag_bytes = bytearray()
    for i in range(0, len(flag_bits), 8):
        if i + 8 > len(flag_bits):
            break
        byte = 0
        for j in range(8):
            byte = (byte << 1) | flag_bits[i + j]
        flag_bytes.append(byte)
    
    return flag_bytes

# Decrypt the flag
try:
    flag_bytes = decrypt_flag('chessboard.pgn')
    print("\nRaw bytes (first 20):", flag_bytes[:20])
    print("\nTrying different encodings:")
    
    # Try different encodings
    encodings = ['ascii', 'utf-8', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            decoded = flag_bytes.decode(encoding)
            print(f"\n{encoding}: {decoded}")
        except Exception as e:
            print(f"{encoding} failed: {str(e)}")
            
    # Print hex representation
    print("\nHex representation:")
    print(' '.join(f'{b:02x}' for b in flag_bytes))
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
    if 'flag_bits' in locals():
        print("Flag bits collected:", len(flag_bits))
        print("Sample bits:", ''.join(str(bit) for bit in flag_bits[:50]))
```
