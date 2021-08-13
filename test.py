import numpy as np
import math
import scipy.special as ss
import random
from gamma_functions import *

# 01_monobit_test.py
def test01(input):
    n = len(input) # Longitud de la cadena
    ones = input.count('1') # Cantidad de 1
    zeroes = input.count('0')    # Cantidad de ceros
    s = abs(ones - zeroes)  
    p = math.erfc(float(s)/(math.sqrt(float(n)) * math.sqrt(2.0))) # Se calcula el valor P

    success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

# 15_random_excursion_variant_test.py 
def test02(input):
    n = len(input) # Longitud de la cadena
    x = list() # Convertir a +1,-2
    for i in range(n):
        x.append(int(input[i],2)*2-1)

    # Sumas parciales
    pos = 0
    s = list()
    for e in x:
        pos = pos+e
        s.append(pos)  

    sprime = [0]+s+[0] # Agregar 0 al inicio y final

    # Ciclos J
    J = 0
    for value in sprime[1:]:
        if value == 0:
            J += 1
            
    # Cantidad de offsets
    count = [0 for x in range(-9,10)]
    for value in sprime:
        if (abs(value) < 10):
            count[value] += 1

    # Obtenemos los valores P
    success = True
    plist = list() # Valores p de cada estado
    p_average = 0.0
    for x in range(-9,10): 
        if x != 0:
            top = abs(count[x]-J)
            bottom = math.sqrt(2.0 * J *((4.0*abs(x))-2.0))
            p = ss.erfc(top/bottom)

            p_average +=p
            plist.append(p)

            success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa



    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

# 06_dft_test.py
def test03(input):
    n = len(input) # Longitud de la cadena
    T = math.sqrt(math.log(1.0/0.05)*n) # Threshold

    N0 = 0.95*n/2.0

    write_array = [0.0,0.0,0.0,0.0]

    ts = list() # Convertir a +1,-1
    for i in range(n):
        if input[i] == '1':
            ts.append(1)
        else:
            ts.append(-1)
    ts_np = np.array(ts)

    fs = np.fft.fft(ts_np)  # Calcular DFT

    half = round(n/2)
    mags = abs(fs)[:half]  # Calcular magnitudes de la primera mitad de la secuencia

    # Contar cuantos quedan arriba del threshold
    N1 = 0.0 
    for mag in mags:
        if mag < T:
            N1 += 1.0
    d = (N1 - N0)/math.sqrt((n*0.95*0.05)/4)
    
    # Clacular valor p
    p = math.erfc(abs(d)/math.sqrt(2))


    success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

# 14_random_excursion_test.py
def test04(input):
    n = len(input)

    # Convertir a +1,-1
    x = list()
    for i in range(n):
        x.append(int(input[i],2)*2 -1 )

    # Sumas parciales
    pos = 0
    s = list()
    for e in x:
        pos = pos+e
        s.append(pos)    
    sprime = [0]+s+[0] # Agrego 0 al inicio y final
    

    # Lista de ciclos
    pos = 1
    cycles = list()
    while (pos < len(sprime)):
        cycle = list()
        cycle.append(0)
        while sprime[pos]!=0:
            cycle.append(sprime[pos])
            pos += 1
        cycle.append(0)
        cycles.append(cycle)
        pos = pos + 1
    
    J = len(cycles)  
    
    vxk = [['a','b','c','d','e','f'] for y in [-4,-3,-2,-1,1,2,3,4] ]

    # Cuento ocurrencias
    for k in range(6):
        for index in range(8):
            mapping = [-4,-3,-2,-1,1,2,3,4]
            x = mapping[index]
            cyclecount = 0
            # Contar en cuantos ciclos cada x ocurre k veces
            for cycle in cycles:
                oc = 0
                # Contar cuantas veces x ocurre en el ciclo
                for pos in cycle:
                    if (pos == x):
                        oc += 1
                # Si x ocurre k veces, incrementar el conteo del ciclo
                if (k < 5):
                    if oc == k:
                        cyclecount += 1
                else:
                    if k == 5:
                        if oc >=5:
                            cyclecount += 1
            vxk[index][k] = cyclecount
    
    # Tabla de referencia de probabilidades aleatorias
    pikx=[[0.5     ,0.25   ,0.125  ,0.0625  ,0.0312 ,0.0312],
          [0.75    ,0.0625 ,0.0469 ,0.0352  ,0.0264 ,0.0791],
          [0.8333  ,0.0278 ,0.0231 ,0.0193  ,0.0161 ,0.0804],
          [0.875   ,0.0156 ,0.0137 ,0.012   ,0.0105 ,0.0733],
          [0.9     ,0.01   ,0.009  ,0.0081  ,0.0073 ,0.0656],
          [0.9167  ,0.0069 ,0.0064 ,0.0058  ,0.0053 ,0.0588],
          [0.9286  ,0.0051 ,0.0047 ,0.0044  ,0.0041 ,0.0531]]
    
    success = True
    plist = list()
    chi_sq = list()
    p_total = 0.0
    for index in range(8):
        # Lista de estados
        mapping = [-4,-3,-2,-1,1,2,3,4] 
        x = mapping[index]
        chisq = 0.0
        for k in range(6):
            top = float(vxk[index][k]) - (float(J) * (pikx[abs(x)-1][k]))
            top = top*top
            bottom = J * pikx[abs(x)-1][k]
            chisq += top/bottom

        p = ss.gammaincc(5.0/2.0,chisq/2.0)
        p_total += p
        plist.append(p)
        chi_sq.append(chisq)

        success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa



    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

# 03_runs_test.py
def test05(input):
    n = len(input)

    ones = input.count('1') # Cantidad de 1
    zeroes = input.count('0') # Cantidad de 0

    prop = float(ones)/float(n)
    tau = 2.0/math.sqrt(n)
    vobs = 0.0

    if abs(prop-0.5) > tau:
        p = 0
    else:
        vobs = 1.0
        for i in range(n-1):
            if input[i] != input[i+1]:
                vobs += 1.0

        p = math.erfc(abs(vobs - (2.0*n*prop*(1.0-prop)))/(2.0*math.sqrt(2.0*n)*prop*(1-prop) ))
    

    success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

def probs(K,M,i):
    M8 =      [0.2148, 0.3672, 0.2305, 0.1875]
    M128 =    [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    M512 =    [0.1170, 0.2460, 0.2523, 0.1755, 0.1027, 0.1124]
    M1000 =   [0.1307, 0.2437, 0.2452, 0.1714, 0.1002, 0.1088]
    M10000 =  [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    if (M == 8):        return M8[i]
    elif (M == 128):    return M128[i]
    elif (M == 512):    return M512[i]
    elif (M == 1000):   return M1000[i]
    else:               return M10000[i]

# 04_longest_run_ones_in_a_block_test.py 
def test06(bits):
    n = len(bits)

    if n < 128:
        return (False,1.0,None)
    elif n<6272:
        M = 8
    elif n<750000:
        M = 128
    else:
        M = 10000
            
    # Valores de K y N
    if M==8:
        K=3
        N=16
    elif M==128:
        K=5
        N=49
    else:
        K=6
        N=75
        
    # Tabla de frecuencias
    v = [0,0,0,0,0,0,0]

    for i in range(N): # Por cada bloque
        # Se encuentra la corrida mas larga
        block = bits[i*M:((i+1)*M)] # Bloque i
        
        run = 0
        longest = 0
        for j in range(M): # Conteo de bits
            if block[j] == 1:
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0

        if M == 8:
            if longest <= 1:    v[0] += 1
            elif longest == 2:  v[1] += 1
            elif longest == 3:  v[2] += 1
            else:               v[3] += 1
        elif M == 128:
            if longest <= 4:    v[0] += 1
            elif longest == 5:  v[1] += 1
            elif longest == 6:  v[2] += 1
            elif longest == 7:  v[3] += 1
            elif longest == 8:  v[4] += 1
            else:               v[5] += 1
        else:
            if longest <= 10:   v[0] += 1
            elif longest == 11: v[1] += 1
            elif longest == 12: v[2] += 1
            elif longest == 13: v[3] += 1
            elif longest == 14: v[4] += 1
            elif longest == 15: v[5] += 1
            else:               v[6] += 1
    
    # Calculo x**2
    chi_sq = 0.0
    for i in range(K+1):
        p_i = probs(K,M,i)
        upper = (v[i] - N*p_i)**2
        lower = N*p_i
        chi_sq += upper/lower
    
    # Calculo p
    p = gammaincc(K/2.0, chi_sq/2.0)
    success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

# 07_non_overlapping_template_matching_test.py
def test07(input):
    n = len(input) # Longitud de la cadena

    # Plantillas de SP800-22rev1a
    templates = [None for x in range(7)]
    templates[0] = [[0,1],[1,0]]
    templates[1] = [[0,0,1],[0,1,1],[1,0,0],[1,1,0]]
    templates[2] = [[0,0,0,1],[0,0,1,1],[0,1,1,1],[1,0,0,0],[1,1,0,0],[1,1,1,0]]
    templates[3] = [[0,0,0,0,1],[0,0,0,1,1],[0,0,1,0,1],[0,1,0,1,1],[0,0,1,1,1],[0,1,1,1,1],
                    [1,1,1,0,0],[1,1,0,1,0],[1,0,1,0,0],[1,1,0,0,0],[1,0,0,0,0],[1,1,1,1,0]]
    templates[4] = [[0,0,0,0,0,1],[0,0,0,0,1,1],[0,0,0,1,0,1],[0,0,0,1,1,1],[0,0,1,0,1,1],
                    [0,0,1,1,0,1],[0,0,1,1,1,1],[0,1,0,0,1,1],
                    [0,1,0,1,1,1],[0,1,1,1,1,1],[1,0,0,0,0,0],
                    [1,0,1,0,0,0],[1,0,1,1,0,0],[1,1,0,0,0,0],
                    [1,1,0,0,1,0],[1,1,0,1,0,0],[1,1,1,0,0,0],
                    [1,1,1,0,1,0],[1,1,1,1,0,0],[1,1,1,1,1,0]]
    templates[5] = [[0,0,0,0,0,0,1],[0,0,0,0,0,1,1],[0,0,0,0,1,0,1],[0,0,0,0,1,1,1],
                    [0,0,0,1,0,0,1],[0,0,0,1,0,1,1],[0,0,0,1,1,0,1],[0,0,0,1,1,1,1],
                    [0,0,1,0,0,1,1],[0,0,1,0,1,0,1],[0,0,1,0,1,1,1],[0,0,1,1,0,1,1],
                    [0,0,1,1,1,0,1],[0,0,1,1,1,1,1],[0,1,0,0,0,1,1],[0,1,0,0,1,1,1],
                    [0,1,0,1,0,1,1],[0,1,0,1,1,1,1],[0,1,1,0,1,1,1],[0,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0],[1,0,0,1,0,0,0],[1,0,1,0,0,0,0],[1,0,1,0,1,0,0],
                    [1,0,1,1,0,0,0],[1,0,1,1,1,0,0],[1,1,0,0,0,0,0],[1,1,0,0,0,1,0],
                    [1,1,0,0,1,0,0],[1,1,0,1,0,0,0],[1,1,0,1,0,1,0],[1,1,0,1,1,0,0],
                    [1,1,1,0,0,0,0],[1,1,1,0,0,1,0],[1,1,1,0,1,0,0],[1,1,1,0,1,1,0],
                    [1,1,1,1,0,0,0],[1,1,1,1,0,1,0],[1,1,1,1,1,0,0],[1,1,1,1,1,1,0]]
    templates[6] = [[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,1,1],[0,0,0,0,0,1,0,1],[0,0,0,0,0,1,1,1],
                    [0,0,0,0,1,0,0,1],[0,0,0,0,1,0,1,1],[0,0,0,0,1,1,0,1],[0,0,0,0,1,1,1,1],
                    [0,0,0,1,0,0,1,1],[0,0,0,1,0,1,0,1],[0,0,0,1,0,1,1,1],[0,0,0,1,1,0,0,1],
                    [0,0,0,1,1,0,1,1],[0,0,0,1,1,1,0,1],[0,0,0,1,1,1,1,1],[0,0,1,0,0,0,1,1],
                    [0,0,1,0,0,1,0,1],[0,0,1,0,0,1,1,1],[0,0,1,0,1,0,1,1],[0,0,1,0,1,1,0,1],
                    [0,0,1,0,1,1,1,1],[0,0,1,1,0,1,0,1],[0,0,1,1,0,1,1,1],[0,0,1,1,1,0,1,1],
                    [0,0,1,1,1,1,0,1],[0,0,1,1,1,1,1,1],[0,1,0,0,0,0,1,1],[0,1,0,0,0,1,1,1],
                    [0,1,0,0,1,0,1,1],[0,1,0,0,1,1,1,1],[0,1,0,1,0,0,1,1],[0,1,0,1,0,1,1,1],
                    [0,1,0,1,1,0,1,1],[0,1,0,1,1,1,1,1],[0,1,1,0,0,1,1,1],[0,1,1,0,1,1,1,1],
                    [0,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0],[1,0,0,1,0,0,0,0],[1,0,0,1,1,0,0,0],
                    [1,0,1,0,0,0,0,0],[1,0,1,0,0,1,0,0],[1,0,1,0,1,0,0,0],[1,0,1,0,1,1,0,0],
                    [1,0,1,1,0,0,0,0],[1,0,1,1,0,1,0,0],[1,0,1,1,1,0,0,0],[1,0,1,1,1,1,0,0],
                    [1,1,0,0,0,0,0,0],[1,1,0,0,0,0,1,0],[1,1,0,0,0,1,0,0],[1,1,0,0,1,0,0,0],
                    [1,1,0,0,1,0,1,0],[1,1,0,1,0,0,0,0],[1,1,0,1,0,0,1,0],[1,1,0,1,0,1,0,0],
                    [1,1,0,1,1,0,0,0],[1,1,0,1,1,0,1,0],[1,1,0,1,1,1,0,0],[1,1,1,0,0,0,0,0],
                    [1,1,1,0,0,0,1,0],[1,1,1,0,0,1,0,0],[1,1,1,0,0,1,1,0],[1,1,1,0,1,0,0,0],
                    [1,1,1,0,1,0,1,0],[1,1,1,0,1,1,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,1,0],
                    [1,1,1,1,0,1,0,0],[1,1,1,1,0,1,1,0],[1,1,1,1,1,0,0,0],[1,1,1,1,1,0,1,0],
                    [1,1,1,1,1,1,0,0],[1,1,1,1,1,1,1,0]]
    
    # Se escoje de manera aleatoria una plantilla
    r = random.SystemRandom()
    template_list = r.choice(templates)
    B = r.choice(template_list)

    m = len(B) # Se obtiene la cantidad de columnas en la plantilla
    N = 8  # Numero de bloques
    M = round(n/N) # Longitud de cada bloque
    
    # Se separan N bloques de M bits
    blocks = list()
    for i in range(N):
        block = list()
        for j in range(M):
            block.append(int(input[i*M+j],2))
        blocks.append(block)

    W=list() # Cantidad de aciertos de la plantilal con cada bloque Wj
    for block in blocks:
        position = 0
        count = 0
        while position < (M-m):

            if block[position:position+m] == B:
                position += m
                count += 1
            else:
                position += 1
        W.append(count)

    # Mu y Sigma
    mu = float(M-m+1)/float(2**m)
    sigma = M * ((1.0/float(2**m))-(float((2*m)-1)/float(2**(2*m))))

    # Prueba x^2
    chi_sq = 0.0
    for j in range(N):
        chi_sq += ((W[j] - mu)**2)/sigma

    p = ss.gammaincc(N/2.0, chi_sq/2.0) # Valor p

    success = ( p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

def normcdf(n):
    return 0.5 * math.erfc(-n * math.sqrt(0.5))

def p_value(n,z):
    sum_a = 0.0
    startk = int(math.floor((((float(-n)/z)+1.0)/4.0)))
    endk   = int(math.floor((((float(n)/z)-1.0)/4.0)))
    for k in range(startk,endk+1):
        c = (((4.0*k)+1.0)*z)/math.sqrt(n)
        #d = scipy.stats.norm.cdf(c)
        d = normcdf(c)
        c = (((4.0*k)-1.0)*z)/math.sqrt(n)
        #e = scipy.stats.norm.cdf(c)
        e = normcdf(c)
        sum_a = sum_a + d - e

    sum_b = 0.0
    startk = int(math.floor((((float(-n)/z)-3.0)/4.0)))
    endk   = int(math.floor((((float(n)/z)-1.0)/4.0)))
    for k in range(startk,endk+1):
        c = (((4.0*k)+3.0)*z)/math.sqrt(n)
        #d = scipy.stats.norm.cdf(c)
        d = normcdf(c)
        c = (((4.0*k)+1.0)*z)/math.sqrt(n)
        #e = scipy.stats.norm.cdf(c)
        e = normcdf(c)
        sum_b = sum_b + d - e 

    p = 1.0 - sum_a + sum_b
    return p
    

# 13_cumulative_sums_test.py 
def test08(input):
    n = len(input)

    # Step 1
    x = list()             # Convert to +1,-1
    for i in range(n):
        #if bit == 0:
        x.append(int(input[i],2)*2-1)
        
    # Steps 2 and 3 Combined
    # Compute the partial sum and records the largest excursion.
    pos = 0
    forward_max = 0
    for e in x:
        pos = pos+e
        if abs(pos) > forward_max:
            forward_max = abs(pos)
    pos = 0
    backward_max = 0
    for e in reversed(x):
        pos = pos+e
        if abs(pos) > backward_max:
            backward_max = abs(pos)
     
    # Step 4
    p_forward  = p_value(n, forward_max)
    p_backward = p_value(n, backward_max)
    
    success = ((p_forward >= 0.01) and (p_backward >= 0.01)) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p_forward, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p_forward, 0] # Se retorna el valor p y que fue fallida


# 12_approximate_entropy_test.py
def test09(input):
    n = len(input)
    m = int(math.floor(math.log(n,2)))-6
    if m < 2:
        m = 2
    if m >3 :
        m = 3
    
    Cmi = list()
    phi_m = list()
    for iterm in range(m,m+2):
        padded_input=input+input[0:iterm-1]

        counts = list()
        for i in range(2**iterm):
            count = 0
            for j in range(n):
                if int(padded_input[j:j+iterm],2) == i:
                    count += 1
            counts.append(count)
    
        Ci = list()
        for i in range(2**iterm):
            Ci.append(float(counts[i])/float(n))
        
        Cmi.append(Ci)
    
        sum = 0.0
        for i in range(2**iterm):
            if (Ci[i] > 0.0):
                sum += Ci[i]*math.log((Ci[i]/10.0))
        phi_m.append(sum)
        
    appen_m = phi_m[0] - phi_m[1]

    chisq = 2*n*(math.log(2) - appen_m)

    p = ss.gammaincc(2**(m-1),(chisq/2.0))
    
    success = (p >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p, 0] # Se retorna el valor p y que fue fallida

# 1_serial_test.py 
def int2patt(n,m):
    pattern = list()
    for i in range(m):
        pattern.append((n >> i) & 1)
    return pattern
    
def countpattern(patt,padded_input,n):
    thecount = 0
    for i in range(n):
        match = True
        for j in range(len(patt)):
            if str(patt[j]) != padded_input[i+j]:
                match = False
                break
        if match:
            thecount += 1
    return thecount

def psi_sq_mv1(m, n, padded_input):
    counts = [0 for i in range(2**m)]
    for i in range(2**m):
        pattern = int2patt(i,m)
        count = countpattern(pattern,padded_input,n)
        counts.append(count)
        
    psi_sq_m = 0.0
    for count in counts: 
        psi_sq_m += (count**2)
    psi_sq_m = psi_sq_m * (2**m)/n 
    psi_sq_m -= n
    return psi_sq_m            
         
def test10(input, patternlen=None):
    n = len(input)

    if patternlen != None:
        m = patternlen  
    else:  
        m = int(math.floor(math.log(n,2)))-2
    
        if m < 4:
            print("Error. Not enough data for m to be 4")
            return [0]*8
        m = 4

    padded_input=input[0:n]+input[0:m-1]
    
    psi_sq_m   = psi_sq_mv1(m, n, padded_input)
    psi_sq_mm1 = psi_sq_mv1(m-1, n, padded_input)
    psi_sq_mm2 = psi_sq_mv1(m-2, n, padded_input)    
    
    delta1 = psi_sq_m - psi_sq_mm1
    delta2 = psi_sq_m - (2*psi_sq_mm1) + psi_sq_mm2

    p1 = ss.gammaincc(2**(m-2),delta1/2.0)
    p2 = ss.gammaincc(2**(m-3),delta2/2.0)
     
    success = (p1 >= 0.01) and (p2 >= 0.01) # Si el valor p es mayor al 1%, la prueba es exitosa

    if (success):
        return [p1, p2, 1] # Se retorna el valor p y que fue exitosa
    else:
        return [p1, p2, 0] # Se retorna el valor p y que fue fallida

print(test01('100010101'))
print(test02('100010101'))
print(test03('100010101'))
print(test04('100010101'))
print(test05('100010101'))
print(test06('100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101'))
print(test07('100010101'))
print(test08('100010101'))
print(test09('100010101'))
print(test10('100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101100010101'))