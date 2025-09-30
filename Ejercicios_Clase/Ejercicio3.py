#Written and Directed By Alvorak
from datetime import date
from typing import List, Optional # usamos Optional para indicar que una variable puede tener un valor de un tipo determinado o ser None


# clase persona: representa a cualquier usuario de la biblioteca
# tanto alumnos como profesores heredan de aquí
class Persona:
    def __init__(self, dni: str, nombre: str, limite_prestamos: int): 
        self.dni = dni                # dni
        self.nombre = nombre          # nombre 
        self.limite_prestamos = limite_prestamos  # limite de libros prestados
        self.prestamos: List["Prestamo"] = []     # lista de préstamos activos y pasados

    # función para prestar un libro o revista
    def prestar(self, elemento: "Elemento", fecha_inicio: date) -> bool:
        # si ya alcanzó el límite no puede
        if len(self.prestamos) >= self.limite_prestamos:
            print(f"{self.nombre} ya alcanzó el límite de préstamos ({self.limite_prestamos}).")
            return False
        # si el elemento ya está prestado no se puede prestar
        if elemento.prestado:
            print(f"el elemento '{elemento.titulo}' ya está prestado.")
            return False

        # se crea el préstamo y se guarda
        prestamo = Prestamo(self, elemento, fecha_inicio)
        self.prestamos.append(prestamo)
        elemento.prestado = True
        return True

    # función para devolver un libro o revista
    def devolver(self, elemento: "Elemento", fecha_fin: date) -> bool:
        for prestamo in self.prestamos:
            # busca el préstamo sin devolver
            if prestamo.elemento == elemento and prestamo.fecha_fin is None:
                prestamo.fecha_fin = fecha_fin
                elemento.prestado = False
                return True
        print(f"{self.nombre} no tiene prestado '{elemento.titulo}'.")
        return False


# clase alumno: hereda de persona pero con un límite de 5 préstamos
class Alumno(Persona):
    def __init__(self, dni: str, nombre: str):
        super().__init__(dni, nombre, limite_prestamos=5)


# clase profesor: hereda de persona pero con un límite de 10 préstamos
class Profesor(Persona):
    def __init__(self, dni: str, nombre: str):
        super().__init__(dni, nombre, limite_prestamos=10)


# clase elemento: representa cualquier cosa que se pueda prestar en la biblioteca
class Elemento:
    def __init__(self, isbn: str, titulo: str):
        self.isbn = isbn          # código isbn
        self.titulo = titulo      # título del elemento
        self.prestado = False     # indica si está prestado o no

    def mostrar_info(self):
        # se implementa en las clases hijas (libro y revista)
        raise NotImplementedError("debe implementarse en la subclase")


# clase libro: hereda de elemento y añade el autor
class Libro(Elemento):
    def __init__(self, isbn: str, titulo: str, autor: str):
        super().__init__(isbn, titulo)
        self.autor = autor

    def mostrar_info(self):
        print(f"libro: {self.titulo} - autor: {self.autor}")


# clase revista: hereda de elemento y añade número y volumen
class Revista(Elemento):
    def __init__(self, isbn: str, titulo: str, numero: int, volumen: int):
        super().__init__(isbn, titulo)
        self.numero = numero
        self.volumen = volumen

    def mostrar_info(self):
        print(f"revista: {self.titulo} - nº {self.numero}, volumen {self.volumen}")


# clase prestamo: relaciona a una persona con un elemento en una fecha
class Prestamo:
    def __init__(self, persona: Persona, elemento: Elemento, fecha_inicio: date):
        self.persona = persona
        self.elemento = elemento
        self.fecha_inicio = fecha_inicio   # fecha en que se prestó
        self.fecha_fin: Optional[date] = None  # fecha en que se devolvió (si ya se devolvió)

    def __str__(self):
        return (f"préstamo: {self.persona.nombre} -> {self.elemento.titulo}, "
                f"inicio: {self.fecha_inicio}, fin: {self.fecha_fin or 'en curso'}")


# Para probar que funcione
if __name__ == "__main__":
    alumno = Alumno("11111111A", "Alvaro")
    profe = Profesor("22222222B", "Maria")

    libro = Libro("ISBN-001", "Fight Club", "Chuck Palahniuk")
    revista = Revista("ISBN-002", "Jueves", 5, 12)

    # el alumno pide un libro
    alumno.prestar(libro, date.today())

    # Intenta coger libro ya prestado
    profe.prestar(libro, date.today())

    # el alumno devuelve libro
    alumno.devolver(libro, date.today())

    # ahora el profesor lo pide
    profe.prestar(libro, date.today())

    # mostramos prestados del profesor
    for prestamo in profe.prestamos:
        print(prestamo)
