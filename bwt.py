import os
import time

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


def invert_bwt(bwt_string):
    
    if not bwt_string:
        return ""
    
    table = ['' for _ in range(len(bwt_string))]
    
    for i in range(len(bwt_string)):
        table = [bwt_string[j] + table[j] for j in range(len(bwt_string))]
        table.sort()
        
    for row in table:
        if row.endswith('$'):
            return row[:-1]  
    
    return ""


def save_to_file(content, filename):
    """Guarda contenido en archivo y retorna tamaño"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return os.path.getsize(filename)

def measure_compression_stage(text, stage_name, transformed_content):
    """Mide tamaño y tiempo para cada etapa"""
    original_size = len(text.encode('utf-8'))
    transformed_size = len(transformed_content.encode('utf-8'))
    
    # Guardar archivos para medición
    original_filename = f"original_{stage_name}.txt"
    transformed_filename = f"{stage_name}_output.txt"
    
    save_to_file(text, original_filename)
    save_to_file(transformed_content, transformed_filename)
    
    ratio = transformed_size / original_size if original_size > 0 else 0
    
    return {
        'stage': stage_name,
        'original_size': original_size,
        'transformed_size': transformed_size,
        'compression_ratio': ratio,
        'original_file': original_filename,
        'output_file': transformed_filename
    }

def bwt_compression_pipeline(text, base_filename):
    """
    Pipeline completo de BWT para compresión
    - Calcula SA
    - Calcula BWT
    - Mide resultados
    """
    print(f"\n PROCESANDO: {base_filename}")
    print(f"   Texto original: {len(text)} caracteres")
    
    # Medir tiempo de suffix Array
    start_time = time.time()
    sa = suffix_array(text + '$')
    sa_time = time.time() - start_time
    
    # Medir tiempo de BWT
    start_time = time.time()
    bwt = build_bwt_for_compression(text, sa)
    bwt_time = time.time() - start_time
    
    # Medir metricas
    metrics = measure_compression_stage(text, "bwt", bwt)
    metrics['sa_time'] = sa_time
    metrics['bwt_time'] = bwt_time
    
    # Verificar reversibilidad
    recovered = invert_bwt(bwt)
    metrics['reversible'] = (text == recovered)
