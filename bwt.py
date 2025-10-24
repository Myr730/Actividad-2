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

def save_bwt_to_file(bwt_string, filename):
    """Guarda BWT en archivo separado - COMO PIDEN LAS INSTRUCCIONES"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(bwt_string)
    print(f"   BWT guardada en: {filename}")
    return True

def load_bwt_from_file(filename):
    """Carga BWT desde archivo - PARA VERIFICAR REVERSIBILIDAD"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip()

def process_text_file(filename, max_chars=5000):
    """
    Procesa un archivo de texto - EVALUACIÓN CON LIBROS COMO PIDEN
    """
    try:
        print(f"\n" + "="*50)
        print(f"PROCESANDO: {filename}")
        print("="*50)
        
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Limitar tamaño para pruebas 
        if max_chars and len(text) > max_chars:
            text = text[:max_chars]
            print(f"   (limitado a {max_chars} caracteres para prueba rapida)")
        
        # calcular Suffix Array
        start_time = time.time()
        sa = suffix_array(text + '$')
        sa_time = time.time() - start_time
        
        # calcular BWT
        start_time = time.time()
        bwt = build_bwt_for_compression(text, sa)
        bwt_time = time.time() - start_time
        
        # Guardar BWT en archivo 
        bwt_filename = f"{os.path.basename(filename)}_bwt.txt"
        save_bwt_to_file(bwt, bwt_filename)
        
        # Verificar reversibilidad desde archivo
        loaded_bwt = load_bwt_from_file(bwt_filename)
        recovered = invert_bwt(loaded_bwt)
        reversible = (text == recovered)
        
        # Calcular metricas - MEDICIoN DE TAMAÑOS
        original_size = len(text.encode('utf-8'))
        bwt_size = len(bwt.encode('utf-8'))
        ratio = bwt_size / original_size
        
        # Mostrar resultados
        print(f"   Resultados:")
        print(f"   - Tamaño original: {original_size} bytes")
        print(f"   - Tamaño BWT: {bwt_size} bytes")
        print(f"   - Ratio: {ratio:.3f}")
        print(f"   - Tiempo SA: {sa_time:.2f}s")
        print(f"   - Tiempo BWT: {bwt_time:.2f}s")
        print(f"   - Reversible: {'SI' if reversible else 'NO'}")
        print(f"   - Archivo BWT: {bwt_filename}")
        
        return {
            'filename': filename,
            'original_size': original_size,
            'bwt_size': bwt_size,
            'ratio': ratio,
            'sa_time': sa_time,
            'bwt_time': bwt_time,
            'reversible': reversible,
            'bwt_file': bwt_filename
        }
        
    except FileNotFoundError:
        print(f"   ERROR: Archivo no encontrado")
        return None
    except Exception as e:
        print(f"   ERROR: {e}")
        return None

if __name__ == "__main__":
    print("SISTEMA DE COMPRESION BWT - PARTE 1")
        # Procesar archivos que existan - EVALUACION CON TXT
    files_to_process = []
    for file in ["Hamlet.txt", "LittleWomen.txt", "MobyDick.txt", "TheCommonReader.txt"]:
        if os.path.exists(file):
            files_to_process.append(file)
    
    if files_to_process:
        results = []
        for file in files_to_process:
            result = process_text_file(file, max_chars=5000)  
            if result:
                results.append(result)
        
        # Reporte  de ESTADISTICAS 
        print(f"\n" + "="*60)
        print("REPORTE FINAL - COMPRESION BWT")
        print("="*60)
        print(f"{'ARCHIVO':<15} {'ORIGINAL':<10} {'BWT':<10} {'RATIO':<8} {'TIEMPO':<8} {'REVERSIBLE'}")
        print("-"*60)
        
        for res in results:
            print(f"{os.path.basename(res['filename']):<15} {res['original_size']:<10} {res['bwt_size']:<10} {res['ratio']:<8.3f} {res['sa_time']+res['bwt_time']:<8.2f} {res['reversible']}")
        
        print(f"\nPROCESAMIENTO COMPLETADO")
        print(f"Archivos BWT generados:")
        for res in results:
            print(f"  - {res['bwt_file']}")
            
    else:
        print("No se encontraron archivos")

