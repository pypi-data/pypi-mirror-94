"""
shuffle.py
A simple package to design shuffled protein sequences to interupt function.

Handles the primary functions
"""

from pipit.backend import backend_shuffle, inverse_shuffle
import random
import os
import csv

def seq(sequence, start, end, number_blocks=1, inverse=False, save=False, output_name="", output_path="", seq_names=True):
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
    number_blocks : int
        the number of sub-regions to shuffle. Increasing this number will increase the
        number of sequences to return.
            Example: 
                shuffle_seq('AAACCCDDD')
                ['AACDDCDAC']
                shuffle_seq('AAACCCDDD', number_blocks=2)
                ['ACAACCDDD', 'AAACDCDDC']
    inverse : bool
        Whether the region specified should be shuffled or held constant.
            If True, the specified region will be held constant and the regions
            outside the sequence will be shuffled.
    save : bool
        Whether to save the sequences to a .csv file or to return them immediately
    output_name : string
        The name of the output .csv file if saving. If no name is given, the file will be 
        saved as pipit_NNNNNNNNNN.csv, where the 10 Ns after pipit_ are replaced by
        10 random alphanumeric characters to avoid overwriting previously generated files.
        Tested the random names up to 100,000 times with no overlap.
    output_path : string
        The path to where to save the .csv file. If no path is given, the file will
        be saved to the current directory.
    seq_names : bool
        If set to true, the output file will designate names for the generated variants.
        The original sequence will be called 'original' and all subsequent variants will
        be called sequence_variant_# where # is replaced by a number.  
    

    Returns
    -----------
    if only one sequence is returned : string
        a string of the shuffled sequence
    if more than one sequence : List
        Returns a list of shuffled sequences
    """


    if inverse==False:
        final_sequences = backend_shuffle(sequence=sequence,
         start=start, end=end, number_blobs=number_blocks, input=False)
    else:
        final_sequences = inverse_shuffle(sequence=sequence,
         start=start, end=end, number_blobs=number_blocks)
    if save==False:
        if len(final_sequences) == 1:
            return final_sequences[0]
        else:
            return final_sequences
    else:
        # add original sequence to the beginning of the final_sequences list
        final_sequences.insert(0, sequence)
        # make list of names of sequences
        sequence_names=[]
        for i in range(0, len(final_sequences)):   
            if i == 0:
                sequence_names.append('original')
            else:
                sequence_names.append('seq_variant_{}'.format(i))
        # if no output name assigned, make a random one.
        if output_name=="":
            possible_vals = 'ABCDEFGHIGJKLMNOPQRSTUVWXYZ123456789'
            temp_val=''.join(random.sample(possible_vals,10))
            output_name = 'pipit_'+temp_val
        # make sure the .csv extension is there
        if output_name[len(output_name)-4:] == ".csv":
            output_name=output_name
        else:
            output_name = output_name + ".csv"        
            # of no ouput path specified save to current directory
        if output_path == "" or output_path == ".":
            output_path = os.getcwd()

        # make sure the slash is in the correct position in the path
        # between the file path and the file name
        if output_path[-1] == "/":
            final_output = "{}{}".format(output_path, output_name)
        else:
            final_output = "{}/{}".format(output_path, output_name)
        try:
            with open(final_output, 'w', newline = '') as csvfile:
                csvWriter = csv.writer(csvfile, dialect='excel')
                if seq_names==True:
                    for i in range(0, len(final_sequences)):
                        csvWriter.writerow([sequence_names[i]])
                        csvWriter.writerow([final_sequences[i]])
                else:
                    for i in range(0, len(final_sequences)):
                        csvWriter.writerow([final_sequences[i]])                 
        # if this fails...
        except IOError:
            # print an error to the console
            print("IO error")

