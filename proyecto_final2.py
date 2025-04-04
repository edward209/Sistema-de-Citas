import csv
import datetime
import os
from tabulate import tabulate
import random
import string

class SistemaCitas:
    def __init__(self):
        self.citas = {}
        self.dentistas = ["Dra. López", "Dr. Martínez", "Dra. Fernández"]
        self.motivos_duracion = {
            "Limpieza": 30,
            "Extracción": 45,
            "Revisión": 20
        }
        self.cargar_citas()

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cargar_citas(self):
        try:
            with open("citas.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.citas[row["ID"]] = {
                        "nombre": row["Paciente"],
                        "fecha": row["Fecha"],
                        "hora": row["Hora"],
                        "duracion": row["Duración"],
                        "dentista": row["Dentista"],
                        "motivo": row["Motivo"],
                        "dias_restantes": int(row["Días Restantes"]),
                        "estado": row["Estado"]
                    }
        except FileNotFoundError:
            pass
    
    def guardar_citas(self):
        with open("citas.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Paciente", "Fecha", "Hora", "Duración", "Dentista", "Motivo", "Días Restantes", "Estado"])
            for id_cita, datos in self.citas.items():
                writer.writerow([id_cita, datos['nombre'], datos['fecha'], datos['hora'], datos['duracion'], datos['dentista'], datos['motivo'], datos['dias_restantes'], datos['estado']])
    
    def mostrar_citas(self):
        self.limpiar_pantalla()
        if not self.citas:
            print("No hay citas registradas.")
        else:
            tabla = []
            for id_cita, datos in self.citas.items():
                # Calcular la diferencia de tiempo entre la cita y el momento actual
                fecha_hora_cita = datetime.datetime.strptime(f"{datos['fecha']} {datos['hora']}", "%Y-%m-%d %H:%M")
                tiempo_restante = fecha_hora_cita - datetime.datetime.now()

                # Calcular los días y las horas restantes
                dias_restantes = tiempo_restante.days
                horas_restantes = tiempo_restante.seconds // 3600  # 3600 segundos en una hora

                # Mostrar días y horas restantes
                tiempo_faltante = f"{dias_restantes} días y {horas_restantes} horas"
                
                # Obtenemos la duración del procedimiento desde el motivo
                duracion = datos['duracion']
                # Mostrar en tabla la información con los nuevos apartados
                tabla.append([
                    id_cita,
                    datos['nombre'],
                    datos['fecha'],
                    datos['hora'],
                    f"{duracion} min",          # Duración
                    tiempo_faltante,            # Tiempo restante
                    datos['estado']
                ])
            
            # Muestra la tabla con los apartados solicitados
            print(tabulate(
                tabla,
                headers=["ID", "Paciente", "Fecha", "Hora", "Duración", "Faltan", "Estado"],
                tablefmt="grid"
            ))
    def validar_nombre(self, nombre):
        # Verificar que el nombre solo contiene letras y espacios
        if not all(c.isalpha() or c.isspace() for c in nombre):
            print("Error: El nombre solo puede contener letras.")
            return False
        return True

    def validar_fecha(self, fecha):
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            print("Error: El formato de la fecha debe ser YYYY-MM-DD.")
            return False

    def validar_hora(self, hora):
        try:
            datetime.datetime.strptime(hora, "%H:%M")
            return True
        except ValueError:
            print("Error: El formato de la hora debe ser HH:MM.")
            return False

    def validar_dentista(self, opcion):
        if opcion.isdigit() and 1 <= int(opcion) <= len(self.dentistas):
            return True
        print("Error: Opción de dentista inválida.")
        return False

    def validar_motivo(self, opcion):
        if opcion.isdigit() and 1 <= int(opcion) <= len(self.motivos_duracion):
            return True
        print("Error: Opción de motivo inválida.")
        return False

    def agendar_cita(self):
        try:
            self.limpiar_pantalla()

            # Generar ID único aleatorio
            while True:
                id_cita = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if id_cita not in self.citas:
                    break
            print(f"ID generado para la cita: {id_cita}")

            while True:
                nombre = input("Nombre del paciente: ")
                if self.validar_nombre(nombre):
                    break

            while True:
                fecha = input("Fecha (YYYY-MM-DD): ")
                if self.validar_fecha(fecha):
                    fecha_hora = datetime.datetime.strptime(f"{fecha} 00:00", "%Y-%m-%d %H:%M")
                    # Validar si la fecha es futura
                    if fecha_hora < datetime.datetime.now():
                        print("Error: La fecha debe ser futura.")
                    else:
                        break

            while True:
                hora = input("Hora (HH:MM): ")
                if self.validar_hora(hora):
                    break

            # Selección de dentista
            print("Seleccione dentista:")
            for i, dentista in enumerate(self.dentistas, start=1):
                print(f"{i}. {dentista}")
            while True:
                opcion_dentista = input("Opción: ")
                if self.validar_dentista(opcion_dentista):
                    dentista = self.dentistas[int(opcion_dentista) - 1]
                    break

            # Selección de motivo
            print("Seleccione motivo de consulta:")
            for i, motivo in enumerate(self.motivos_duracion.keys(), start=1):
                print(f"{i}. {motivo}")
            while True:
                opcion_motivo = input("Opción: ")
                if self.validar_motivo(opcion_motivo):
                    motivo = list(self.motivos_duracion.keys())[int(opcion_motivo) - 1]
                    duracion = self.motivos_duracion[motivo]
                    break

            # Validar fecha
            fecha_hora = datetime.datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if fecha_hora < datetime.datetime.now():
                print("Error: La fecha debe ser futura.")
                return

            dias_restantes = (fecha_hora - datetime.datetime.now()).days
            estado = "Vigente"

            self.citas[id_cita] = {
                "nombre": nombre,
                "fecha": fecha,
                "hora": hora,
                "duracion": str(duracion),
                "dentista": dentista,
                "motivo": motivo,
                "dias_restantes": dias_restantes,
                "estado": estado
            }
            self.guardar_citas()
            print("Cita agendada exitosamente.")
        except ValueError:
            print("Error: Formato de fecha u hora incorrecto.")

    def actualizar_cita(self):
        self.limpiar_pantalla()
        id_cita = input("Ingrese ID de la cita a actualizar: ")
        if id_cita not in self.citas:
            print("Error: ID no encontrado.")
            return
        
        print("Deje en blanco si no desea modificar un campo.")
        nombre = input(f"Nombre actual ({self.citas[id_cita]['nombre']}): ") or self.citas[id_cita]['nombre']
        dentista = input(f"Dentista actual ({self.citas[id_cita]['dentista']}): ") or self.citas[id_cita]['dentista']
        motivo = input(f"Motivo actual ({self.citas[id_cita]['motivo']}): ") or self.citas[id_cita]['motivo']
        
        self.citas[id_cita].update({"nombre": nombre, "dentista": dentista, "motivo": motivo})
        self.guardar_citas()
        print("Cita actualizada correctamente.")
    
    def eliminar_cita(self):
        self.limpiar_pantalla()
        id_cita = input("Ingrese ID de la cita a eliminar: ")
        if id_cita in self.citas:
            del self.citas[id_cita]
            self.guardar_citas()
            print("Cita eliminada correctamente.")
        else:
            print("Error: ID no encontrado.")
    
    def menu(self):
        while True:
            self.limpiar_pantalla()
            print("\nBienvenido a OdontoLeon Clinica Dental")
            print("1. Mostrar citas")
            print("2. Agendar cita")
            print("3. Actualizar cita")
            print("4. Eliminar cita")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.mostrar_citas()
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.agendar_cita()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.actualizar_cita()
                input("Presione Enter para continuar...")
            elif opcion == "4":
                self.eliminar_cita()
                input("Presione Enter para continuar...")
            elif opcion == "5":
                print("Gracias por preferirnos...")
                break
            else:
                print("Opción inválida, intente nuevamente.")
                input("Presione Enter para continuar...")

if __name__ == "__main__":
    sistema = SistemaCitas()
    sistema.menu()