"""
Ejercicio 1:
Diseña una aplicación para un ayuntamiento donde se puedan efectuar y registrar pagos. Para ello, se deben registrar unos ciertos usuarios, que 
podrán ser ciudadanos normales que quieran pagar sus impuestos o funcionarios que sean capaces de eliminar o crear nuevos pagos. 
Los pagos tendrán un importe, una fecha de creación, un estado "Pago pendiente" o "Finalizado", además de una fecha de pago en el caso de que se hayan finalizado. 
Desde el ayuntamiento se debe poder hacer, como mínimo:

Dar de alta o de baja a nuevos usuarios y funcionarios.
Creación y eliminación de pagos, siempre a través de un cierto funcionario.
Listar todos los pagos, pudiendo filtrar por ciudadano, por fecha de inicio (indica un cierto intervalo), 
por fecha de fin (indica un cierto intervalo). También se pueden combinar estos filtros.

Ejercicio 2: Excepciones

Piensa e implementa al menos dos excepciones para este programa.
"""
from datetime import datetime, MAXYEAR, MINYEAR, date, timedelta

class UsuarioNoExiste(Exception):
    def __init__(self, ciudadano, *args):
        super().__init__(*args)
        self._ciudadano = ciudadano
    
    def __str__(self):
        return f"El usuario {self._ciudadano.nombre +' ' + self._ciudadano.apellidos} no pertenece al ayuntamiento."
    

class Usuario:
    def __init__(self, nombre, apellidos, documento):
        self.nombre = nombre
        self.apellidos = apellidos
        self.documetno = documento 

    @property #con property defino el getter y hado del atributo de solo lectura
    def documento(self):
        return self.documento

    def mostrar_info(self):
        print(f'Usuario con nomnbre {self.nombre + self.apellidos} y documento {self.documetno}')


class Ciudadano(Usuario):
    def __init__(self, nombre, apellidos, documento):
        super().__init__(nombre, apellidos, documento)
        self._pagos = list() #defino una lista de pagos para el ciudadano
    
    def add_pago(self, pago):
        self._pagos.append(pago) #con esto añadimos un pago al ciudadano

    def mostrar_info(self):
        print('Ciudadano:')
        super().mostrar_info()

class Funcionario(Usuario):
    def __init__(self, nombre, apellidos, documento):
        super().__init__(nombre, apellidos, documento)

    def crear_pago():
        pass


    def eliminar_pago():
        pass


    def mostrar_info(self):
        print('Funcionario:')
        super().mostrar_info()
        

class Pago:
    num_pagos = 0 #Variable estatica para llevar cuenta de todos los pagos realizados
    def __init__(self, importe: float, ciudadano: Ciudadano, funcionario : Funcionario):
        Pago.num_pagos +=1
        self._id = Pago.num_pagos
        self._importe = importe
        self._ciudadano = ciudadano
        self._fechaInicio = datetime.now().date()
        self._fechaPago = None 
        self._creador = funcionario #Funcionario que crea esto
        ciudadano.add_pago(self) #Añado un pago al ciudadano

    def pagar(self):
        self._fechaPago = datetime.now() #guardamos hasta el momento de pago
    
    #Vamos a hacer los getters que necesitemos
    @property
    def ciudadano(self):
        return self._ciudadano
    
    @property
    def id(self):
        return self._id
    
    @property
    def fecha_inicio(self):
        return self._fechaInicio
    
    @property
    def fecha_pago(self):
        return self._fechaPago
    
    @property
    def estado(self):
        return "Finalizado" if self._fechaPago else "Pago pendiente" #Si la fecha poago es null/none
    
class Ayuntamiento():
    def __init__(self, ciudad):
        self.ciudad = ciudad
        self._listaCiudadadanos = list()
        self._listaFuncionarios = list()
        self._listaPagos = list()

    def crearUsuario(self, newUser:Usuario):
        if isinstance(newUser, Funcionario):
            self._listaFuncionarios.append(newUser)
        elif isinstance(newUser, Ciudadano):
            self._listaCiudadadanos.append(newUser)

    def borrarUsuario(self, user: Usuario):
        for i, users in enumerate(self._listaCiudadadanos):
            if users.documento == user.documento:
                self._listaCiudadadanos.pop(i)
                return
        
        for i, users in enumerate(self._listaFuncionarios):
            if users.documento == user.documento:
                self._listaFuncionarios.pop(i)
                return
        

    def crearPago(self, importe: float, ciudadano: Ciudadano, funcionario: Funcionario):
        if ciudadano not in self._listaCiudadadanos:
            raise UsuarioNoExiste(ciudadano)
        pago = Pago(ciudadano=ciudadano,funcionario=funcionario,importe=importe)
        self._listaPagos.append(pago)

    

    def eliminarPago(self, id: int):
        for i, pago in enumerate(self._listaPagos):
            if pago.id == id:
                self._listaPagos.pop(i)

    def listaPagos(self, dni = None,fechaInicioCreación=date(year=MINYEAR, month=1, day=1),
                    fechaFinCreación=date(year=MAXYEAR, month=12, day=31),
                    fechaInicioPago=date(year=MINYEAR, month=1, day=1),
                    fechaFinPago=date(year=MAXYEAR, month=12, day=31)):
        def filtroDni(pago: Pago):
            if dni: 
                return pago.ciudadano.dni == dni
            else:
                return True

        def filtroCreación(pago: Pago):
            return fechaInicioCreación <= pago.fecha_inicio <= fechaFinCreación

        def filtroPago(pago: Pago):
            # Nos aseguramos de que exista una fecha de pago
            return (pago.fecha_pago is None) or fechaInicioPago <= pago.fecha_pago <= fechaFinPago

        return list(filter(filtroPago, filter(filtroCreación, filter(filtroDni, self._listaPagos))))


if __name__ == '__main__':
    ayuntamiento = Ayuntamiento("Pozuelo")

    #Usuarios
    ciudadanoModelo = Ciudadano("Jaime", "Orbea", "231231")
    ciudadanoModelo2 = Ciudadano("Alvaro", "Garcia", "111111")

    funcionario = Funcionario("Juan", "Garcia", "111111")

    #ayuntamiento.crearUsuario(ciudadanoModelo)
    ayuntamiento.crearUsuario(ciudadanoModelo2)
    ayuntamiento.crearUsuario(funcionario)

    ciudadanoModelo.mostrar_info()
    ciudadanoModelo2.mostrar_info()
    funcionario.mostrar_info()

    ayuntamiento.crearPago(150, ciudadanoModelo, funcionario)
    ayuntamiento.crearPago(200.4, ciudadanoModelo2, funcionario)
    ayuntamiento.crearPago(1233.4, ciudadanoModelo2, funcionario)

    ayuntamiento.listaPagos()

    ayuntamiento._listaPagos[0].pagar()

    ayuntamiento.eliminarPago(ayuntamiento._listaPagos[0].id)

    ayuntamiento.listaPagos()

    print("Pagos realizados en los últimos 2 días:")
    fecha_inicio = (datetime.now() - timedelta(days=2)).date()
    fecha_fin = datetime.now().date()
    for p in ayuntamiento.listaPagos(fechaInicioPago=fecha_inicio, fechaFinPago=fecha_fin):
        print(f"  ID {p.id}: ciudadano {p._ciudadano.nombre}, pagado el {p.fecha_pago}")




    