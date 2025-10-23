class SubstrRank:
    def __init__(self, left_rank=0, right_rank=0, index=0):
        self.left_rank = left_rank
        self.right_rank = right_rank
        self.index = index

def make_ranks(substr_rank, n):
    r = 1
    rank = [-1] * n
    rank[substr_rank[0].index] = r
    for i in range(1, n):
        if (substr_rank[i].left_rank != substr_rank[i-1].left_rank or
			substr_rank[i].right_rank != substr_rank[i-1].right_rank):
            r += 1
        rank[substr_rank[i].index] = r
    return rank

def suffix_array(T):
    n = len(T)
    substr_rank = []

    for i in range(n):
        substr_rank.append(SubstrRank(ord(T[i]), ord(T[i + 1]) if i < n-1 else 0, i))

    substr_rank.sort(key=lambda sr: (sr.left_rank, sr.right_rank))

    l = 2
    while l < n:
        rank = make_ranks(substr_rank, n)

        new_substr_rank = []
        for i in range(n):
            new_substr_rank.append(SubstrRank(
                rank[i], 
                rank[i + l] if i + l < n else 0, 
                i  
            ))
        
        substr_rank = new_substr_rank
        substr_rank.sort(key=lambda sr: (sr.left_rank, sr.right_rank))
        l *= 2

    SA = [sr.index for sr in substr_rank]

    return SA

def build_bwt_for_compression(text, suffix_array):
    text_with_terminal = text + '$'
    n = len(text_with_terminal)
    
    bwt_chars = []
    for i in range(n):
        #caracter  BWT
        sa_pos = suffix_array[i] 
        
        if sa_pos == 0:
            bwt_char = text_with_terminal[-1]
        else:
            bwt_char = text_with_terminal[sa_pos - 1]
        bwt_chars.append(bwt_char)
    
    return ''.join(bwt_chars)

if __name__ == "__main__":
    test_text = "mississippi"
    sa = suffix_array(test_text + '$')
    bwt = build_bwt_for_compression(test_text, sa)
    print(f"Texto: {test_text}")
    print(f"BWT: {bwt}")

