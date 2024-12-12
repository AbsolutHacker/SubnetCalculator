# Anforderungskriterien:
# Die maximale Anzahl der zur Verfügung stehenden IP-Adressen und die davon abhängigen Host-Adressen müssen
# dargestellt werden
# Die Broadcastadresse muss ausgegeben werden -----------------
# Die Netzwerkadresse muss ausgegeben werden -----------------
# Die Netzmaske muss in der CIDR-Notation ausgegeben werden
# die Anzahl der Netzwerk- und Host-Bits muss ausgegeben werden.
# die Umrechnung erfolgt grafisch nachvollziehbar und nur mit Hilfe von Grundrechenarten (ggf. modulo und Potenzrechnung).
# Es soll keine Makro-Programmierung unter Excel stattfinden oder unter Python keine (Fremd-) Bibliotheken eingesetzt werden.
# Netzwerk- und Hostanteil müssen durch farbige Hinterlegung der Bits grafisch deutlich werden

TGREEN =  '\033[42m' # Green text
TBLUE =  '\033[44m' # Blue highlighter
ENDC = '\033[m' # Reset color

input_ip = input('Bitte geben sie die IP Adresse ein: ')
input_mask = input('Bitte geben sie die Subnetzmaske ein: ')

print('\nWir teilen die IP Adresse in ihre Oktette auf diese sehen dann so aus')
def dotted_decimal_to_bitfield(string: str):
    result = [0, 0, 0, 0]
    octets = [ int(octet) for octet in string.split('.') ]
    i = 0
    for octet in octets:
        if octet > 255 or octet < 0:
            raise ValueError('Value out of range: ' + str(octet))
        result[i] = octet
        i += 1
    return (result[0] << 24) + (result[1] << 16) + (result[2] << 8) + result[3]

def bitfield_to_dotted_decimal(bitfield: int):
    octets = [ int((bitfield >> 24) & 0xFF), int((bitfield >> 16) & 0xFF), int((bitfield >> 8) & 0xFF), int(bitfield & 0xFF) ]
    return '.'.join(map(str, octets))

def bitfield_to_binary(bitfield: int, highlight_bits: int = -1):
    output = ''
    for i in range(0, 32):
        if i < highlight_bits:
            # TODO: färben
            output += TGREEN
        else:
            output += TBLUE
        offset = 31 - i
        output += str((bitfield >> offset) & 0x1)
        if offset % 8 == 0 and offset > 0:
            output += '.'
    return output + ENDC

addr = dotted_decimal_to_bitfield(input_ip)
print('\nBinärewer der Ip Adresse: ' + str(dotted_decimal_to_bitfield(input_ip)))

if '.' in input_mask:
    mask = dotted_decimal_to_bitfield(input_mask)
else:
    # TODO: das noch richtig machen
    mask = -1 << (32 - int(input_mask))

nwad = addr & mask
bcad = nwad | (~mask)
print('\nDie Adressen in Übersicht:')
print('\nDie IP-Adresse: ' + bitfield_to_dotted_decimal(addr))
print('Binär: ')
print('Die Subnetzmaske: ' + bitfield_to_dotted_decimal(mask))
print('Die Netzadresse: ' + bitfield_to_dotted_decimal(nwad))
print('Die Broadcastadresse: ' + bitfield_to_dotted_decimal(bcad))

