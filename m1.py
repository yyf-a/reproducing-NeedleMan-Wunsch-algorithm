import numpy as np

# Useful constants
gap_penalty = -1
match_award = 1
mismatch= -1

# define a function returns the marks for base alignment
def matching(base1, base2):
    if base1 == base2:
        return match_award
    elif base1 == '-' or base2 == "-":
        return gap_penalty
    else:
        return mismatch

def nw_algorithm(seq1, seq2):
    # build scoring matrix of sequences
    
    n_rows = len(seq1)
    n_columns = len(seq2)

    scoring_matrix = np.zeros((n_rows + 1, n_columns + 1))

    # fill first row and columns
    scoring_matrix[:,0] = np.linspace(0, -n_rows, n_rows + 1)
    scoring_matrix[0,:] = np.linspace(0, -n_columns, n_columns + 1)

    for i in range(1, n_rows + 1):
        for j in range(1, n_columns + 1):
            # calculate and compare all three cases:
            match = scoring_matrix[i - 1][j - 1] + matching(seq1[i - 1], seq2[j - 1])
            seq1_gap = scoring_matrix[i][j - 1] + gap_penalty
            seq2_gap = scoring_matrix[i - 1][j] + gap_penalty
            scoring_matrix[i,j] = max(match, seq1_gap, seq2_gap)

    # tracing back with two tracing strings
    seq1_trac = ""
    seq2_trac = ""

    # from the bottom right corner
    i = n_rows
    j = n_columns
    while i > 0 and j > 0: # end touching the top or the left edge
        score = scoring_matrix[i][j]
        diagonal = scoring_matrix[i-1][j-1]
        up = scoring_matrix[i-1][j]
        left = scoring_matrix[i][j-1]
            
        # Check what is previous score
        if score == diagonal + matching(seq1[i-1], seq2[j-1]):
            seq1_trac += seq1[i-1]
            seq2_trac += seq2[j-1]
            i -= 1
            j -= 1
        elif score == up + gap_penalty:
            seq1_trac += seq1[i-1]
            seq2_trac += '-'
            i -= 1
        elif score == left + gap_penalty:
            seq1_trac += '-'
            seq2_trac += seq2[j-1]
            j -= 1

        # Finish tracing up to the top left cell
    while j > 0:
        seq1_trac += '-'
        seq2_trac += seq2[j-1]
        j -= 1
    while i > 0:
        seq1_trac += seq1[i-1]
        seq2_trac += '-'
        i -= 1
        
    # the records are reversed
    align_seq1 = seq1_trac[::-1]
    align_seq2 = seq2_trac[::-1]
    print(align_seq1)
    print(align_seq2)


print('Enter first sequence:')
seq1 = input()
print('Enter second sequence:')
seq2 = input()
nw_algorithm(seq1, seq2)