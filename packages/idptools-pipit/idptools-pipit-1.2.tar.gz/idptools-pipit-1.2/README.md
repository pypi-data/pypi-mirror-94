PIPIT
==============================

# *P*roteins *I*nto s*P*ecific random*I*zed segmen*T*s

## What is PIPIT?

**PIPIT** is a simple package to design shuffled protein sequences to interupt function. Specifically, by specifying the protein region to shuffle as well as the size of sequence 'blocks' to shuffle, you can quickly generate variants that will allow you to rapidly interrogate the function of specific protein regions by changing the order of amino acids in that region.

How do you use PIPIT?
PIPIT can be used within Python or from the terminal.


## Installation:

From PyPi, just use

    $ pip install idptools-pipit

To clone the GitHub repository and gain the ability to modify a local copy of the code, run

    $ git clone https://github.com/allOfTheGoodUsernamesWereTaken/PIPIT.git
    $ cd PIPIT
    $ pip install .

This will install PIPIT locally.

## Command-line usage - 

To use PIPIT from the command-line just use the ``pipit-shuffle`` command. There are 3 required inputs for this command that *must be input in the following order*.

1. The sequence to be shuffled
2. The number of the starting residue of the region of the sequence to either shuffle **which is default** or hold constant **if inverse is specified** (more on that later)
3. The number of the ending residue of the region of the sequence to either shuffle **which is default** or hold constant **if inverse is specified**

Example - 

    $ pipit-shuffle SSSSMSEGSHPRKTNDDQAN 5 15
    $ ['SSSSMPERNTSKSGHDDQAN']

Importantly, the region specified *to be shuffled* will include the residues specified as the start of the region and the end. So in this example, residues 1, 2, 3, and 4 as well as 16, 17, 18, 19, and 20 will be constant whereas residues 5-15 can be shuffled.

### Additonal flags

``-n`` or ``--number`` will allow you to specify the number of sequence blocks to break up the shuffled region into. *NOTE* - If the number of blocks specified is not compatible with the length of the region to be shuffled, a warning will be printed letting you know. However, the sequences will still be generated, and the leftover residues will be added to the minimal number of blocks such that the total number of residues equals the length of the region to be shuffled.

``-i`` or ``--inverse`` will make it so that the region you specify will be held constant and the regions outside of the specified region will be shuffled.

``-s`` or ``--save`` will allow you to save the output sequences as a .csv file as opposed to simply printing to the terminal.

``-name`` or ``--file_name`` will allow you to specify the name of the output .csv file. If a name is not specified, the default name will be pipit_NNNNNNNNNN.csv where NNNNNNNNNN is ten random numbers and letters. The random letters and numbers help avoid situations where files are accidentally overwritten

``-path`` or ``--output_path`` will allow you to specify the path to which to save the generated .csv file. By default, the file will be saved to the current directory.

``-names`` or ``--seq_names`` will give the generated sequences arbitrary names. The original sequence will be called 'original', and each subsequent sequence will be called sequence_variant_# where # is a number starting at 1 that increases per variant generated. If names are not used, the top sequence (or first sequence) is always the original.

#### Examples

Specifying sequence number where the region to be shuffled is divisible by the number of sequence blocks

    $ pipit-shuffle ACDEFGHIKLMNPQRSTVWY 5 16 -n 2
    $ ['ACDEIFKGLHMNPQRSTVWY', 'ACDEFGHIKLRMQSNPTVWY']

Specifying sequence number where the region to be shuffled is **NOT** divisible by the number of sequence blocks

    $ pipit-shuffle ACDEFGHIKLMNPQRSTVWY 5 15 -n 2
    $ Warning: specified number of blobs does not result in equal number of residues per blob.
    $ ['ACDEHLKFGIMNPQRSTVWY', 'ACDEFGHIKLQPNRMSTVWY']

Using the inverse flag

    $ pipit-shuffle ACDEFGHIKLMNPQRSTVWY 5 15 -i
    $ ['ADECFGHIKLMNPQRSTVWY', 'ACDEFGHIKLMNPQRYVWTS']

When using the inverse flag, each side of the sequence is treated as a sequence block. So in this example, the first sequence shown after the command is used has the first 4 residues shuffled whereas the second sequence has the last 5 residues shuffled. Importantly, the coordinates for teh residues to keep constant include the number specified, so in this example residues 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, and 15 are not shuffled.

## Python usage - 

PIPIT can also be used within Python. After installing PIPIT, first you need to import PIPIT - 
 
    import pipit
    from pipit import shuffle

### Shuffling sequences in Python

To shuffle sequences in Python, use the seq function - 

    shuffle.seq(sequence, start, end)

Where sequence is the sequence you want to shuffle, start is the starting residue number you want to shuffle and end is the number of the final residue you want to shuffle.

Example - 

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15)
    'ACDEHFNMQGLPRKISTVWY'

#### Specifying number of sequnce blocks to shuffle

If you want to break up your shufled region into multiple discrete shuffled blocks, simply specify 

    shuffle.seq(sequence, start, end, number_blocks=N)

where N is some integer number that is less than the length of the sequence to be shuffled.

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 16, number_blocks=2)
    ['ACDEIKHFLGMNPQRSTVWY', 'ACDEFGHIKLRQMPSNTVWY']

*Note* - now that multiple sequences are generated, the sequences are returned as a list of strings as opposed to a single string.

***Important*** - if the length of the region to be shuffle dis not divisible by the number of blocks specified, a warning will be printed to the user. However, the sequences will still be generated, and the leftover residues will be added to the minimal number of blocks such that the total number of residues equals the length of the region to be shuffled.

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15, number_blocks=2)
    Warning: specified number of blobs does not result in equal number of residues per blob.
    ['ACDEKFIHGLMNPQRSTVWY', 'ACDEFGHIKLPRMQNSTVWY']

#### Specifying a region to keep constant

If you want to specify a region to *NOT SHUFFLE* as opposed to a region to shuffle (which is the default behavior for PIPIT), simply set inverse=True

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15, inverse=True)
    ['ECADFGHIKLMNPQRSTVWY', 'ACDEFGHIKLMNPQRVYWST']

When using the inverse flag, each side of the sequence is treated as a sequence block. So in this example, the first sequence shown after the command is used has the first 4 residues shuffled whereas the second sequence has the last 5 residues shuffled. Importantly, the coordinates for teh residues to keep constant include the number specified, so in this example residues 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, and 15 are not shuffled.

#### Saving sequences as an output .csv file

If you want to sve your sequences, you can set save=True. This will result in your sequenecs being saved as a .csv file.

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15, inverse=True, save=True)

By default, file name will be pipit_NNNNNNNNNN.csv where NNNNNNNNNN is ten random numbers and letters. The random letters and numbers help avoid situations where files are accidentally overwritten. Additionally, the default is to save the file to the current working directory.

#### Specifying the file name

You can specify the name of the generated file by setting output_name="name_of_cool_file". You can add the .csv extension, otherwise PIPIT will add it for you.

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15, inverse=True, save=True, output_name='my_shuffled_seqs')

#### Specifying the output path

Specifying output path can be done by setting output_path equal to the path to where to save the .csv file. 

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15, inverse=True, save=True, output_path='/Users/me/Desktop/cool_sequence_folder')

#### Removing arbirary sequence names from the generated .csv file

By default when using PIPIT from Python, the sequences will be arbitrarily named. The original sequence will be called 'original', and each subsequent sequence will be called sequence_variant_# where # is a number starting at 1 that increases per variant generated. If names are not used, the top sequence (or first sequence) is always the original. This can be done by setting seq_names=False

Example:

    shuffle.seq('ACDEFGHIKLMNPQRSTVWY', 5, 15, inverse=True, save=True, seq_names=False)



### Copyright

Copyright (c) 2021, Ryan Emenecker Washington University School of Medicine


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.
