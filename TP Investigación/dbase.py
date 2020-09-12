import pandas as pd
import os
import curses
# pip install windows-curses
# libreria para las interfaces.

menu = []


class Generador:
    def __init__(self, row):
        self.nombre = row["Fabricante"] + " - " + row["Modelo"]
        self.altura = row["Altura (mts)"]
        self.radio = row["Radio (mts)"]
        self.curva = {}
        # cargo el atributo curva con los valores del excel.
        x = 0
        for i in range(52):
            # para que busque la columna '0.Xms' en el renglón.
            columna_excel = "{0:0.1f}ms".format(x)
            self.curva[columna_excel] = row[columna_excel]
            x += 0.5

    def potenciaGenerada(self, viento):
        # devuelvo 0 si me da valores fuera del intervalo.
        if viento <= 0 or viento >= 25.5:
            return 0

        # recorro haciendo pasos de a 0.5 y devuelvo el valor de potencia que caiga en el intervalo valido.
        c = 0
        for i in self.curva.keys():
            if viento >= c:
                if viento < c + 0.5:
                    return self.curva[i]
            c += 0.5

    def MostrarDatos(self):
        print(" ------------------ Aerogenerador seleccionado -------------------")
        print("          " + self.nombre)
        print("          Altura: " + str(self.altura))
        print("          Radio: " + str(self.radio))
        print(" -----------------------------------------------------------------")


def ObtenerGenerador():

    # busca el archivo de excel
    dir_file = os.path.dirname(os.path.abspath(__file__))
    dir_db = dir_file + "/database/power_curves.xlsx"
    data = pd.read_excel(r"{}".format(dir_db))

    # Para cada renglón de datos, obtengo sus valores en las columnas correspondientes
    for i in range(len(data)):
        row = str(data.loc[i].at["Fabricante"]).ljust(25) + "│"
        row += str(data.loc[i].at["Modelo"]).ljust(18) + "│"
        row += ("      " + str(data.loc[i].at["Altura (mts)"]).ljust(8)) + "│"
        row += "   " + str(data.loc[i].at["Radio (mts)"])
        menu.append(row)

    # invoca al menu.
    fila_seleccionada = curses.wrapper(main)
    # busco entre los datos la fila seleccionada.
    renglon = data.loc[fila_seleccionada]
    # Creo un objeto generador con los valores que corresponden al renglon seleccionado
    generador = Generador(renglon)
    generador.MostrarDatos()

    return generador


# ----------------------------------------- codigo para las interfaces graficas ------------------------------------- #

def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    stdscr.addstr(0, 5, "Seleccione modelo de generador")
    stdscr.addstr(2, 5, "Fabricante               │ Modelo           │ Altura (mts) │ Radio (mts)")
    stdscr.addstr(3, 5, "─────────────────────────┼──────────────────┼──────────────┼─────────────")
    for idx, row in enumerate(menu):
        x = 5
        y = 4 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def main(stdscr):

    # inicializa la pantalla.
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # especifica cual es la columna seleccionada.
    current_row = 0

    # muestra el menu principal.
    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < (len(menu) - 1):
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            break
        print_menu(stdscr, current_row)
    return current_row
