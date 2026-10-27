import logging

# 1. CONFIGURACIÓN DEL LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('sistema_fj.log', mode='w', encoding='utf-8'), logging.StreamHandler()]
)

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
    def __init__(self, id_cliente, nombre, correo):
        super().__init__(id_cliente)
        self._nombre = nombre
        self._correo = None
        self.set_correo(correo)

    def set_correo(self, correo):
        if "@" not in correo:
            raise ErrorValidacion(f"Correo inválido: {correo}")
        self._correo = correo

    def obtener_detalles(self):
        return f"Cliente: {self._nombre} | Correo: {self._correo}"

# 5. CLASE ABSTRACTA SERVICIO Y DERIVADOS (Polimorfismo)
class Servicio(Entidad):
    def __init__(self, id_servicio, nombre):
        super().__init__(id_servicio)
        self.nombre = nombre
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0): # Método sobrecargado
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
            logging.info(f"Iniciando reserva de {self.cliente._nombre} para {self.servicio.nombre}")
            
            if duracion <= 0:
                raise ErrorValidacion("La duración debe ser mayor a 0 horas.")
            
            if estado_servicio == "caido":
                try:
                    raise ConnectionError("Error 504 - Timeout de red")
                except ConnectionError as e:
                    raise ServicioNoDisponible("El servicio no está disponible.") from e
            
            costo = self.servicio.calcular_costo(duracion, impuesto=0.19, descuento=5000)
            self.estado = "Confirmada"
        
        except ErrorValidacion as e:
            logging.error(f"Error de validación: {e}")
            self.estado = "Fallida"
        except ServicioNoDisponible as e:
            logging.error(f"Error de servicio: {e} | Causa: {e.__cause__}")
            self.estado = "Fallida"
        except Exception as e:
            logging.critical(f"Error inesperado: {e}")
            self.estado = "Fallida"
        else:
            logging.info(f"Reserva exitosa. Costo total: ${costo}")
        finally:
            logging.info(f"Finalizado proceso de reserva. Estado final: {self.estado}\n")

# 7. SIMULACIONES (10 OPERACIONES COMPLETAS)
if __name__ == "__main__":
    print("=== SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    
    # Simulaciones (Válidas e Inválidas)
    try:
        c1 = Cliente(1, "Ana", "ana@correo.com")
        c2 = Cliente(2, "Pedro", "pedro_correo.com") # Inválido
    except ErrorValidacion as e:
        logging.error(f"Fallo al crear cliente: {e}")
        c2 = Cliente(2, "Pedro", "pedro@correo.com") # Corregido

    s1 = ReservaSala(1, "Sala VIP")
    s2 = AlquilerEquipo(2, "Laptop Gamer")
    s3 = AsesoriaEspecializada(3, "Asesoría en Python")

    # 1. Reserva Válida
    Reserva(c1, s1).procesar(2)
    # 2. Reserva Válida
    Reserva(c1, s2).procesar(5)
    # 3. Reserva Inválida (Duración 0)
    Reserva(c2, s3).procesar(0)
    # 4. Reserva Inválida (Servicio caído)
    Reserva(c2, s1).procesar(3, "caido")
    # 5. Reserva Válida
    Reserva(c1, s3).procesar(1)
    # 6. Reserva Válida
    Reserva(c2, s2).procesar(10)
    # 7. Inválida (Duración negativa)
    Reserva(c1, s1).procesar(-2)
    # 8. Inválida (Servicio caído)
    Reserva(c1, s2).procesar(2, "caido")
    # 9. Válida
    Reserva(c2, s3).procesar(4)
    # 10. Válida
    Reserva(c1, s1).procesar(8)

    print("=== SIMULACIONES COMPLETADAS. REVISA EL ARCHIVO sistema_fj.log ===")