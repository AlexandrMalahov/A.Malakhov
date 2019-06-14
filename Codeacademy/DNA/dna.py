"""DNA Analysis."""

SAMPLE = ['GTA', 'GGG', 'CAC']
# DNA sample taken from the crime scene.


def read_dna(dna_file):
    """Sample DNA reading."""

    dna_data = ''
    with open(dna_file, 'r') as _f:
        for line in _f:
            dna_data += line
    return dna_data


def dna_codons(dna):
    """DNA dividing into codons."""

    codons = []
    for i in range(0, len(dna), 3):
        if (i + 3) < len(dna):
            codons.append(dna[i:i + 3])
    return codons


def match_dna(dna):
    """Codon versus suspect DNA."""

    matches = 0
    for codon in dna:
        if codon in SAMPLE:
            matches += 1
    return matches


def is_criminal(dna_sample):
    """
    This method will do all the hard work
    of reading a DNA sample from a suspect,
    comparing it to a DNA sample from the crime scene,
    and letting the user know whether
    the suspect is a criminal.
    """

    dna_data = read_dna(dna_sample)
    codons = dna_codons(dna_data)
    num_matches = match_dna(codons)
    if num_matches >= 3:
        print "# of codon matches: %s. DNA profile matches. Continue investigation." % num_matches
    else:
        print "# of codon matches: %s. Suspect may be free." % num_matches


is_criminal("suspect1.txt")
is_criminal("suspect2.txt")
is_criminal("suspect3.txt")
