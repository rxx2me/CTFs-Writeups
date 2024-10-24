# Given DNA sequence and its conversion
dna_sequence = "GTT GCA TAT ATA TCC GCC CGG GTA AGT AAC CGT ATA TGT AAG CGT TGG CAG GTA TAT GTA CAT GTA TAC GGG CTC GAA TAT ACG TTG GTG TAA CTG TAT AAG GGT TCG AGT GAG TAC TAG AGA GTT GGA TAG AGT AGT CGC ATG AAT ACT CGT TGG AGT ATT GGA GTG AAT ACT CGT TGG GCT AGG TGG CGG TCT GGC TGG ACG AGC GTT CGC ATG GGC GCC TG"

#from here : https://dnacode.bc.cas.cz/index.php?ln=en
converted_sequence = "vayisarvsnrickrwqvyvhvygleytlv.lykgsseyorvgossrmntrwsigvntrwarwrsgwtsvrmgatg"

# Convert DNA to binary
# Assume: A = 00, C = 01, G = 10, T = 11
dna_to_binary = {
    'A': '00',
    'C': '01',
    'G': '10',
    'T': '11'
}

# Convert the DNA sequence to binary
binary_sequence = ''.join([dna_to_binary[base] for base in dna_sequence.replace(' ', '')])

# Reverse the binary sequence
reversed_binary_sequence = binary_sequence[::-1]

# Convert binary to text
def binary_to_text(binary_str):
    text = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        text += chr(int(byte, 2)) if len(byte) == 8 else ""
    return text

# Convert the binary sequence to text
binary_to_text_output = binary_to_text(binary_sequence)

# Convert the reversed binary sequence to text
reversed_binary_to_text_output = binary_to_text(reversed_binary_sequence)

# Print the binary sequence and the reversed binary sequence along with their corresponding text
print("Original Binary Sequence:", binary_sequence)
print("Reversed Binary Sequence:", reversed_binary_sequence)
print("Reversed Binary Sequence (Text):", reversed_binary_to_text_output)