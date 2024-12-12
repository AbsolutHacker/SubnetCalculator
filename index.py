# Anforderungskriterien:
# Die maximale Anzahl der zur Verfügung stehenden IP-Adressen und die davon abhängigen Host-Adressen müssen
# dargestellt werden
# Die Broadcastadresse muss ausgegeben werden
# Die Netzwerkadresse muss ausgegeben werden
# Die Netzmaske muss in der CIDR-Notation ausgegeben werden
# die Anzahl der Netzwerk- und Host-Bits muss ausgegeben werden.
# die Umrechnung erfolgt grafisch nachvollziehbar und nur mit Hilfe von Grundrechenarten (ggf. modulo und Potenzrechnung).
# Es soll keine Makro-Programmierung unter Excel stattfinden oder unter Python keine (Fremd-) Bibliotheken eingesetzt werden.
# Netzwerk- und Hostanteil müssen durch farbige Hinterlegung der Bits grafisch deutlich werden

input_ip = input('Bitte geben sie die IP Adresse ein ')
input_mask = input('bitte geben sie die Subnetzmaske ein ')

print('Wir teilen die IP Adresse in ihre Oktette auf diese sehen dann so aus')
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

addr = dotted_decimal_to_bitfield(input_ip)

if '.' in input_mask:
    mask = dotted_decimal_to_bitfield(input_mask)
else:
    # TODO: das noch richtig machen
    mask = -1 << (32 - int(input_mask))

nwad = addr & mask
bcad = nwad | (~mask)

print('Die IP-Adresse: ' + bitfield_to_dotted_decimal(addr))
print('Die Subnetzmaske: ' + bitfield_to_dotted_decimal(mask))
print('Die Netadresse: ' + bitfield_to_dotted_decimal(nwad))
print('Die Brodcastadresse: ' + bitfield_to_dotted_decimal(bcad))

