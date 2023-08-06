"""
shuffle.py
A simple package to design shuffled protein sequences to interupt function.

Handles the primary functions
"""

from pipit.backend import backend_shuffle, inverse_shuffle

def shuffle_seq(sequence, start, end, number_blobs=1, inverse=False):
    """ 
    Function that holds functionality for PIPIT. By default, will just shuffle 
    the entire sequence. If inverese=True, the start and end of the sequence
    must be specified.
    
    Parameters
    ------------
    sequence : string
        sequence to be shuffled
    start : int
        the starting amino acid to either be shuffled (standard) or kept constant (inverse)
    end : int
        the ending amino acid to either be shuffled (standard) or kept constant (inverse)
    number_blobs : int
        the number of sub-regions to shuffle. Increasing this number will increase the
        number of sequences to return.
            Example: 
                shuffle_seq('AAACCCDDD')
                ['AACDDCDAC']
                shuffle_seq('AAACCCDDD', number_blobs=2)
                ['ACAACCDDD', 'AAACDCDDC']
    inverse : bool
        Whether the region specified should be shuffled or held constant.
            If True, the specified region will be held constant and the regions
            outside the sequence will be shuffled.
    

    Returns
    -----------
    Default : List
        Returns a list of shuffled sequences
    """


    if inverse==False:
        final_sequences = backend_shuffle(sequence=sequence,
         start=start, end=end, number_blobs=number_blobs, input=False)
        return final_sequences
    else:
        final_sequences = inverse_shuffle(sequence=sequence,
         start=start, end=end, number_blobs=number_blobs)
        return final_sequences




