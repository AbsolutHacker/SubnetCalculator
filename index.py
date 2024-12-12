#!/usr/bin/env python3

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

def dotted_decimal_to_bitfield(string: str):
    # wir kopieren hier in eine vor-genullte Liste, um die Angabe "unvollständiger"
    # Adressen zu unterstützen, z.B. 10/8
    result = [0, 0, 0, 0]
    octets = [ int(octet) for octet in string.split('.') ]
    i = 0
    for octet in octets:
        if octet > 255 or octet < 0:
            raise ValueError('Value out of range: ' + str(octet))
        result[i] = octet
        i += 1
    return (result[0] << 24) + (result[1] << 16) + (result[2] << 8) + result[3]

def cidr_mask_to_bitfield(cidr_mask: int):
    all_ones = int(-1)
    mask = all_ones << (32 - cidr_mask)
    truncated_mask = mask & 0xFFFFFFFF
    return truncated_mask

def bitfield_to_cidr_mask(bitfield: int):
    negated_bitfield = ~bitfield & 0xFFFFFFFF
    ones = 0
    while negated_bitfield & 0x1 == 0x1:
        ones += 1
        negated_bitfield = negated_bitfield >> 1
    return 32 - ones

def bitfield_to_dotted_decimal(bitfield: int):
    octets = [ int((bitfield >> 24) & 0xFF), int((bitfield >> 16) & 0xFF), int((bitfield >> 8) & 0xFF), int(bitfield & 0xFF) ]
    return '.'.join(map(str, octets))

def bitfield_to_binary(bitfield: int, highlight_bits: int = -1):
    output = ''
    for i in range(0, 32):
        if i < highlight_bits:
            output += TGREEN
        else:
            output += TBLUE
        offset = 31 - i
        output += str((bitfield >> offset) & 0x1)
        if offset % 8 == 0 and offset > 0:
            output += '.'
    return output + ENDC

# -------- MAIN --------

input_ip = input('Bitte geben Sie die IP-Adresse ein: ')

if '/' in input_ip:
    input_ip, input_mask = input_ip.split('/')
else:
    input_mask = input('Bitte geben Sie die Subnetzmaske ein: ')

addr = dotted_decimal_to_bitfield(input_ip)

if '.' in input_mask:
    mask = dotted_decimal_to_bitfield(input_mask)
else:
    mask = cidr_mask_to_bitfield(int(input_mask))

nwad = addr & mask
bcad = nwad | (~mask)
cidr_mask = bitfield_to_cidr_mask(mask)
host_bits = 32 - cidr_mask

print('\nDie Adressen in Übersicht:')
print('\nDie IP-Adresse: ' + bitfield_to_dotted_decimal(addr) + '/' + str(cidr_mask))
print('Binär: ' + bitfield_to_binary(addr, cidr_mask))
print('Die Subnetzmaske: ' + bitfield_to_dotted_decimal(mask))
print('Binär: ' + bitfield_to_binary(mask, cidr_mask))
print('Die Netzadresse: ' + bitfield_to_dotted_decimal(nwad) + '/' + str(cidr_mask))
print('Binär: ' + bitfield_to_binary(nwad, cidr_mask))
print('Die Broadcastadresse: ' + bitfield_to_dotted_decimal(bcad))
print('Binär: ' + bitfield_to_binary(bcad, cidr_mask))

print('\n' + TGREEN + str(cidr_mask) + ' Netz-Bits,' + ENDC + ' ' + TBLUE + str(host_bits) + ' Host-Bits' + ENDC)
print(str(2**host_bits) + ' Adressen insgesamt, davon ' + str((2**host_bits) - 2) + ' für Hosts verfügbar')
