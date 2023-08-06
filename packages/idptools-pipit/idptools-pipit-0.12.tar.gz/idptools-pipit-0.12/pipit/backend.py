"""
holds backend functionality for shuffle.py
"""

import random


def backend_shuffle(sequence, start, end, number_blobs=1, input=False):
    """
    Function that will return sequences where each blob is shuffled
    Does whole sequence. It doesn't have to be called backend_shuffle,
    but I thought it was kind of funny...

    Parameters
    ------------
    sequence : string
        sequence to be shuffled
    start : int
        the starting amino acid to be shuffled
    end : int
        the ending amino acid to be shuffled
    number_blobs : int
        the number of sub-regions to shuffle. Increasing this number will increase the
        number of sequences to return.
            Example: 
                backend_shuffle('AAACCCDDD')
                ['AACDDCDAC']
                backend_shuffle('AAACCCDDD', number_blobs=2)
                ['ACAACCDDD', 'AAACDCDDC']
    input : bool
        Whether the function will be used as input for another function.
        This only changes whether a warning is printed when the number of 
        blobs is incompatible with the sequence lenght.
    

    Returns
    -----------
    Default : List
        Returns a list of shuffled sequences

    """
    # sanity check
    if number_blobs==0:
        raise Exception('Number of blobs must be greater than 0')
    if number_blobs > end-start:
        raise Exception('The number of blobs cannot be greater than the number of residues in the sequence')
    if start > end:
        raise Exception('The value for end must be greater than start.')

    # make a list to hold the generated sequences
    sequence_list = []
    # pull out sequence to be shuffled
    seq_to_shuffle = sequence[start-1:end]
    # get other parts of sequence
    if start == 1:
        seq_part_1 = ""
    else:
        seq_part_1 = sequence[0:start-1]
    if end == len(sequence):
        seq_part_2 = ""
    else:
        seq_part_2 = sequence[end:]
    # store the length of the sequence to be shuffled
    length_seq_shuff = len(seq_to_shuffle)
    # figure out blob length
    blob_length = int(length_seq_shuff/number_blobs)
    # figure out if any blobs need to be bigger 
    if blob_length * number_blobs < length_seq_shuff:
        # figure out number of blobs that need to be bigger
        number_bigger_blobs = length_seq_shuff % number_blobs
        # let the user know (if not being used as input for a second function)
        if input==False:
            print("Warning: specified number of blobs does not result in equal number of residues per blob.")
    else:
        # don't need any bigger blobs
        number_bigger_blobs = 0

    # figure out blob size to get whole sequence
    cur_residue = 0
    for blob in range(0, number_blobs):
        if number_bigger_blobs != 0:
            end_blob = blob_length + 1
            number_bigger_blobs = number_bigger_blobs - 1
        else:
            end_blob = blob_length
        current_block = seq_to_shuffle[cur_residue:cur_residue + end_blob]
        shuffled_block = ''.join(random.sample(current_block,len(current_block)))
        if cur_residue == 0:
            final_sequence = seq_part_1 + shuffled_block + seq_to_shuffle[cur_residue + end_blob:] + seq_part_2
        elif blob == number_blobs-1:
            final_sequence = seq_part_1 + seq_to_shuffle[0:cur_residue] + shuffled_block + seq_part_2
        else:
            final_sequence = seq_part_1 + seq_to_shuffle[0:cur_residue] + shuffled_block + seq_to_shuffle[cur_residue + end_blob:] + seq_part_2
        sequence_list.append(final_sequence)
        cur_residue = cur_residue + end_blob
    return sequence_list



def inverse_shuffle(sequence, start, end, number_blobs=1):
    """
    Function that will return sequences where each the specified
    region is held constant and the rest of the sequence is shuffled

    Parameters
    ------------
    sequence : string
        sequence to be shuffled
    start : int
        the starting amino acid to be kept constant
    end : int
        the ending amino acid to be kept constant
    number_blobs : int
        the number of sub-regions to shuffle. Increasing this number will increase the
        number of sequences to return.
    

    Returns
    -----------
    Default : List
        Returns a list of shuffled sequences

    """    
    # sanity check
    if number_blobs==0:
        raise Exception('Number of blobs must be greater than 0')
    if number_blobs > end-start:
        raise Exception('The number of blobs cannot be greater than the number of residues in the sequence')
    if start > end:
        raise Exception('The value for end must be greater than start.')

    # get the static sequence
    static_seq = sequence[start-1:end]
    # get the static bits when the first or second part are being shuffled
    static_shuffle_1 = sequence[:start-1]
    static_shuffle_2 = sequence[end:]
    # get the parts to shuffle
    shuffle_1 = sequence[:start-1]
    shuffle_2 = sequence[end:]

    # check if blob length is compatible with shuffle sequence length
    # store the length of the sequence to be shuffled
    length_seq_shuff_1 = len(shuffle_1)
    length_seq_shuff_2 = len(shuffle_2)
    # figure out blob lengths
    blob_length_1 = int(length_seq_shuff_1/number_blobs)
    blob_length_2 = int(length_seq_shuff_2/number_blobs)
    # figure out if the blob length is compatible with sequence length
    if blob_length_1 * number_blobs < length_seq_shuff_1:
        print("Warning: specified number of blobs for first part of sequence does not result in equal number of residues per blob.")
    if blob_length_2 * number_blobs < length_seq_shuff_2:
        print("Warning: specified number of blobs for second part of sequence does not result in equal number of residues per blob.")
    # shuffle the sequences
    shuffled_1 = backend_shuffle(shuffle_1, start=1, end=len(shuffle_1)+1, number_blobs = number_blobs, input=True)
    shuffled_2 = backend_shuffle(shuffle_2, start=1, end=len(shuffle_2)+1, number_blobs = number_blobs, input=True)
    # build the sequence list
    sequence_list = []
    for shuff_1 in shuffled_1:
        cur_sequence = shuff_1 + static_seq + static_shuffle_2
        sequence_list.append(cur_sequence)
    for shuff_2 in shuffled_2:
        cur_sequence = static_shuffle_1 + static_seq + shuff_2
        sequence_list.append(cur_sequence)
    return sequence_list







