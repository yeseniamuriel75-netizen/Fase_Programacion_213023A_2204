import logging
import re

# >>>>>>>>>> INICIO CAMBIO 1 - Integrante 4 (Mateo Betancur Ospina): configuración profesional del archivo de logs
# 1. CONFIGURACIÓN DEL LOGGING
from logging.handlers import RotatingFileHandler  # Manejador que limita el tamaño del archivo de log
from pathlib import Path  # Permite construir rutas de archivos de forma segura en Windows, Linux y macOS

RUTA_LOG = Path(__file__).resolve().parent / "sistema_fj.log"  # El log se crea junto al programa, sin importar desde dónde se ejecute
FORMATO_LOG = "%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s"  # Fecha, nivel, función y línea de origen, mensaje
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"  # Fecha legible sin milisegundos (ej. 2026-11-17 20:15:03)

manejador_archivo = RotatingFileHandler(  # Escribe los eventos en el archivo sistema_fj.log
    RUTA_LOG,
    mode="a",  # "a" = añadir: conserva el historial de todas las sesiones (antes "w" lo borraba en cada ejecución)
    maxBytes=1_000_000,  # Cuando el archivo llega a ~1 MB se rota para que no crezca sin límite
    backupCount=3,  # Se guardan hasta 3 copias anteriores: sistema_fj.log.1, .2 y .3
    encoding="utf-8",  # Permite tildes y ñ en los mensajes
)
manejador_archivo.setLevel(logging.DEBUG)  # El archivo guarda TODO, incluidos los detalles técnicos (DEBUG)

manejador_consola = logging.StreamHandler()  # Muestra los eventos en la terminal
manejador_consola.setLevel(logging.INFO)  # La consola solo muestra INFO o superior, para no saturar al usuario

logging.basicConfig(  # Aplica la configuración al registrador raíz que usan todas las llamadas logging.*()
    level=logging.DEBUG,  # Nivel mínimo global; cada manejador filtra después según su propio nivel
    format=FORMATO_LOG,
    datefmt=FORMATO_FECHA,
    handlers=[manejador_archivo, manejador_consola],
)
# <<<<<<<<<< FIN CAMBIO 1

# 2. EXCEPCIONES PERSONALIZADAS
class ErrorValidacion(Exception): pass
class ServicioNoDisponible(Exception): pass

# 3. CLASE ABSTRACTA
class Entidad:
    def __init__(self, id_entidad):
        self.id_entidad = id_entidad
    def obtener_detalles(self):
        raise NotImplementedError("Método abstracto")

# 4. CLASE CLIENTE (Encapsulación y Validaciones)
class Cliente(Entidad):
    def __init__(self, id_cliente: int, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre  # Activa @nombre.setter
        self.correo = correo  # Activa @correo.setter
    
    @property
    def id_cliente(self) -> int:
        return self.id_entidad
    
    @id_cliente.setter
    def id_cliente(self, valor: int):
        self.id_entidad = valor

    # --- Encapsulación y Validación de Nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorValidacion("El nombre del cliente no puede estar vacío.")
        if len(valor.strip()) < 2:
            raise ErrorValidacion(f"Nombre inválido ('{valor}'). Debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    # --- Encapsulación y Validación de Correo ---
    @property
    def correo(self) -> str:
        return self._correo
    
    @correo.setter
    def correo(self, valor: str):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not isinstance(valor, str) or not re.match(patron_email, valor.strip()):
            raise ErrorValidacion(f"Correo electrónico inválido: '{valor}'. Formato requerido: usuario@dominio.com")
        self._correo = valor.strip()

    def obtener_detalles(self):
        return f"Cliente ID: {self.id_cliente} | Nombre: {self.nombre} | Correo: {self.correo}"
        
# 5. CLASE ABSTRACTA SERVICIO Y DERIVADOS (Polimorfismo)
class Servicio(Entidad):
    def __init__(self, id_servicio, nombre):
        super().__init__(id_servicio)
        self.nombre = nombre
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        raise NotImplementedError
    def obtener_detalles(self):
        return f"Servicio: {self.nombre}"

class ReservaSala(Servicio):
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        costo_base = duracion_horas * 50000
        return (costo_base * (1 + impuesto)) - descuento

class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        costo_base = duracion_horas * 30000
        return (costo_base * (1 + impuesto)) - descuento

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        costo_base = duracion_horas * 80000
        return (costo_base * (1 + impuesto)) - descuento

# 6. CLASE RESERVA (Integración y Excepciones)
class Reserva:
    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"
   
    def procesar(self, duracion, estado_servicio="activo"):
        try:
            logging.info(f"Iniciando reserva de {self.cliente.nombre} para el servicio: {self.servicio.nombre}")
            
            if duracion <= 0:
                raise ErrorValidacion("La duración debe ser mayor a 0 horas.")
            
            if estado_servicio == "caido":
                try:
                    raise ConnectionError("Error 504 - Timeout de red")
                except ConnectionError as e:
                    raise ServicioNoDisponible("El servicio no está disponible en este momento.") from e
            
            costo = self.servicio.calcular_costo(duracion, impuesto=0.19, descuento=5000)
            # CAMBIO 2 - Integrante 4 (Mateo): detalle técnico del cálculo; solo queda en el archivo (nivel DEBUG)
            logging.debug(f"Cálculo: servicio={type(self.servicio).__name__}, horas={duracion}, impuesto=0.19, descuento=5000, costo={costo}")
            self.estado = "Confirmada"
        
        except ErrorValidacion as e:
            logging.error(f"Error de validación: {e}")
            self.estado = "Fallida"
        except ServicioNoDisponible as e:
            logging.error(f"Error de servicio: {e} | Causa: {e.__cause__}")
            self.estado = "Fallida"
        except Exception as e:
            # CAMBIO 3 - Integrante 4 (Mateo): exc_info=True guarda en el log la traza completa del error inesperado
            logging.critical(f"Error inesperado: {e}", exc_info=True)
            self.estado = "Fallida"
        else:
            logging.info(f"Reserva exitosa. Costo total: ${costo}")
        finally:
            logging.info(f"Finalizado proceso de reserva. Estado final: {self.estado}\n")

# 7. MENÚ INTERACTIVO PARA CAPTURAS REALES
if __name__ == "__main__":
    s1 = ReservaSala(1, "Sala VIP")
    s2 = AlquilerEquipo(2, "Laptop Gamer")
    s3 = AsesoriaEspecializada(3, "Asesoría en Python")
    
    servicios_disponibles = {"1": s1, "2": s2, "3": s3}
    logging.info("===== INICIO DE SESIÓN DEL SISTEMA SOFTWARE FJ =====")  # CAMBIO 4 - Integrante 4 (Mateo): separa cada ejecución en el historial del log

    while True:
        print("\n=== SISTEMA INTEGRAL SOFTWARE FJ (MENÚ INTERACTIVO) ===")
        print("1. Registrar nueva reserva (Ingresar datos desde cero)")
        print("2. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "2":
            print("Saliendo del sistema. ¡Hasta luego!")
            logging.info("===== FIN DE SESIÓN =====\n")  # CAMBIO 4 - Integrante 4 (Mateo): cierre de sesión registrado
            break
            
        if opcion == "1":
            try:
                print("\n--- DATOS DEL CLIENTE ---")
                id_c = int(input("Ingrese ID del cliente (número): "))
                nom = input("Ingrese nombre del cliente: ")
                email = input("Ingrese correo electrónico: ")
                
                # Creación del cliente (validará automáticamente con los setters)
                cliente_actual = Cliente(id_c, nom, email)
                
                print("\n--- SELECCIONE UN SERVICIO ---")
                print("1. Sala VIP ($50,000/hr)")
                print("2. Laptop Gamer ($30,000/hr)")
                print("3. Asesoría en Python ($80,000/hr)")
                
                s_op = input("Elija el servicio (1-3): ").strip()
                if s_op not in servicios_disponibles:
                    print("❌ Opción de servicio inválida.")
                    logging.warning(f"Servicio inválido seleccionado: {s_op!r}")  # CAMBIO 5 - Integrante 4 (Mateo)
                    continue
                
                servicio_actual = servicios_disponibles[s_op]
                
                dur = float(input("Ingrese la duración en horas: "))
                
                estado_serv = "activo"
                simular_caida = input("¿Simular caída de red/servidor? (s/n): ").strip().lower()
                if simular_caida == 's':
                    estado_serv = "caido"
                
                print("\n--- PROCESANDO RESERVA ---")
                reserva = Reserva(cliente_actual, servicio_actual)
                reserva.procesar(dur, estado_serv)
                
            except ValueError as e:
                print("❌ Error de formato: Ingrese valores numéricos válidos donde corresponda.")
                logging.warning(f"Dato con formato inválido ingresado por el usuario: {e}")  # CAMBIO 5 - Integrante 4 (Mateo): antes este error no quedaba en el log
            except ErrorValidacion as e:
                logging.error(f"Error de validación en consola: {e}")
            except Exception as e:
                logging.critical(f"Error inesperado: {e}", exc_info=True)  # CAMBIO 3 - Integrante 4 (Mateo): traza completa en el log
        else:
            print("❌ Opción no válida. Intente de nuevo.")
            logging.warning(f"Opción de menú inválida: {opcion!r}")  # CAMBIO 5 - Integrante 4 (Mateo): registro de opciones inválidas
