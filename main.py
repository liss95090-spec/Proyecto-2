import time
from machine import Pin, PWM

# ==========================================
# CONFIGURACIÓN DE HARDWARE (Pines Físicos)
# ==========================================
BOTON_PIN = Pin(15, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(14))

pines_salida_circuito = [
    Pin(10, Pin.OUT),  # Bit 0 (LSB)
    Pin(11, Pin.OUT),  # Bit 1       
    Pin(12, Pin.OUT),  # Bit 2       
    Pin(13, Pin.OUT)   # Bit 3 (MSB) 
]

MORSE_A_ASCII = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z'
}

UMBRAL_PUNTO_RAYA = 0.25   
TIEMPO_ESPACIO_LETRA = 0.6  


def inyectar_bits_a_compuertas(valor_ascii):
    """
    Aísla los 4 bits menos significativos del carácter ASCII (Máscara 0x0F)
    y envía los estados lógicos corregidos con lógica invertida y orden estándar.
    """
    cuatro_bits = valor_ascii & 0x0F
    
    # Extraer el valor real de cada bit individual (0 o 1) de menor a mayor peso
    bit0 = (cuatro_bits >> 0) & 1  # LSB (GP10)
    bit1 = (cuatro_bits >> 1) & 1  # (GP11)
    bit2 = (cuatro_bits >> 2) & 1  # (GP12)
    bit3 = (cuatro_bits >> 3) & 1  # MSB (GP13)
    
    # Generar el string binario teórico correcto (MSB a LSB) para la consola
    string_binario = f"{bit3}{bit2}{bit1}{bit0}"
    
    # === CORRECCIÓN DE LÓGICA INVERTIDA CON ORDEN CORRECTO ===
  
    pines_salida_circuito[0].value(1 - bit0)  # GP10 recibe Bit 0 corregido
    pines_salida_circuito[1].value(1 - bit1)  # GP11 recibe Bit 1 corregido
    pines_salida_circuito[2].value(1 - bit2)  # GP12 recibe Bit 2 corregido
    pines_salida_circuito[3].value(1 - bit3)  # GP13 recibe Bit 3 corregido
        
    return string_binario

def controlar_buzzer(estado):
    if estado:
        buzzer.freq(800)
        buzzer.duty_u16(32768)
    else:
        buzzer.duty_u16(0)

# ==========================================
# BUCLE PRINCIPAL DE CONTROL
# ==========================================
codigo_morse_acumulado = ""
ultimo_cambio_estado = time.time()
boton_presionado_antes = False

print("=== CONSOLA DE TRADUCCIÓN MAQUETA ACTIVA ===")
print("Presiona el botón conectado en GP15...")

while True:
    estado_actual_boton = BOTON_PIN.value()
    tiempo_actual = time.time()
    
    if estado_actual_boton == 1 and not boton_presionado_antes:
        controlar_buzzer(True)
        tiempo_presionado_inicio = time.time()
        boton_presionado_antes = True
        ultimo_cambio_estado = tiempo_actual
        
    elif estado_actual_boton == 0 and boton_presionado_antes:
        controlar_buzzer(False)
        duracion_pulso = time.time() - tiempo_presionado_inicio
        
        if duracion_pulso < UMBRAL_PUNTO_RAYA:
            codigo_morse_acumulado += "."
        else:
            codigo_morse_acumulado += "-"
            
        boton_presionado_antes = False
        ultimo_cambio_estado = tiempo_actual
        
    if not boton_presionado_antes and len(codigo_morse_acumulado) > 0:
        if (tiempo_actual - ultimo_cambio_estado) > TIEMPO_ESPACIO_LETRA:
            
            if codigo_morse_acumulado in MORSE_A_ASCII:
                letra = MORSE_A_ASCII[codigo_morse_acumulado]
                valor_ascii_decimal = ord(letra)
                
                bits_str = inyectar_bits_a_compuertas(valor_ascii_decimal)
                
                print(f" Morse: {codigo_morse_acumulado:5} | Letra: {letra} | "
                      f"ASCII: {valor_ascii_decimal:3} | Bits enviados a compuertas: [{bits_str}]")
            else:
                print(f" Código Morse [{codigo_morse_acumulado}] desconocido.")
                
            codigo_morse_acumulado = ""
            
    time.sleep(0.01)