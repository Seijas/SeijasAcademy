#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import sqlite3 as dbapi
from informes import Informes

__author__ = 'Seijas'


class Panel:

    db = dbapi.connect("database.db")
    cursor = db.cursor()

    def __init__(self, user):
        file = "./views/panel.glade"
        builder = Gtk.Builder()
        builder.add_from_file(file)

        signals = {
            "b_borrar": self.b_borrar,
            "b_insertar": self.b_insertar,
            "b_buscar": self.b_buscar,
            "on_MainPanel_destroy": Gtk.main_quit
        }

        builder.connect_signals(signals)

        self.ide = builder.get_object("entry_id")
        self.nome = builder.get_object("entry_nombre")
        self.idade = builder.get_object("entry_edad")
        self.b_borrar = builder.get_object("button_borrar")
        self.b_insertar = builder.get_object("button_insertar")
        self.b_buscar = builder.get_object("button_buscar")
        self.view = builder.get_object("students")
        self.error = builder.get_object("label_error")
        self.menu_bar = builder.get_object("menu_bar")

        render = Gtk.CellRendererText()

        columna1 = Gtk.TreeViewColumn("ID", render, text=0)
        columna2 = Gtk.TreeViewColumn("Nombre", render, text=1)
        columna3 = Gtk.TreeViewColumn("Edad", render, text=2)

        self.view.append_column(columna1)
        self.view.append_column(columna2)
        self.view.append_column(columna3)

        self.menu_bar.set_hexpand(True)

        menuitem = Gtk.MenuItem(label="File")
        self.menu_bar.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="Said 'Hola'")
        menuitem.connect_object("activate", self.menu_warning, ["Seijas Academy", "Hello " + user + "!"])
        menu.append(menuitem)
        menuitem = Gtk.SeparatorMenuItem()
        menu.append(menuitem)
        # menuitem = Gtk.MenuItem(label="Close Session")
        # menuitem.connect_object("activate", self.menu_close_session(self), None)
        # menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="Exit")
        menuitem.connect_object("activate", Gtk.main_quit, "close")
        menu.append(menuitem)

        menuitem = Gtk.MenuItem(label="Informes")
        self.menu_bar.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="new registration")
        menuitem.connect_object("activate", self.print_new_registration, None)
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="monthly bill")
        menuitem.connect_object("activate", self.print_monthly_bill, None)
        menu.append(menuitem)

        menuitem = Gtk.MenuItem(label="Ayuda")
        self.menu_bar.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="Acerca de")
        menuitem.connect_object("activate", self.menu_warning, ["Acerca de...", "Created by Seijas"])
        menu.append(menuitem)

        self.menu_bar.show_all()

        self.update_list()

    def menu_warning(self, text):
        window = Gtk.Window(title=text[0])
        label = Gtk.Label(text[1])
        label.set_padding(100, 30)
        window.add(label)
        window.connect("delete-event", self.close)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

    def close(self, widget, none):
        widget.destroy()

    def menu_close_session(self, control):
        Gtk.main_quit
        from main import Login
        Login()

    @staticmethod
    def print_new_registration(control):
        Informes(1)

    @staticmethod
    def print_monthly_bill(control):
        Informes(0)

    def update_list(self):
        lista = Gtk.ListStore(str, str, int)
        self.cursor.execute("select * from students order by id")

        for fila in self.cursor:
            lista.append(fila)

        self.view.set_model(lista)
        self.view.show()

    def clean_inserts(self):
        self.ide.set_text("")
        self.nome.set_text("")
        self.idade.set_text("")

    def raise_error(self, string=""):
        self.error.set_text(string)

    def b_borrar(self, control):
        self.raise_error()
        id = self.ide.get_text()
        name = self.nome.get_text()
        age = self.idade.get_text()

        if id != "":
            if name == "" and age == "":
                self.cursor.execute("delete from students where id='" + id + "';")
            elif name == "" and age != "":
                self.cursor.execute("delete from students where id='" + id + "' and age=" + age + ";")
            elif name != "" and age == "":
                self.cursor.execute("delete from students where id='" + id + "' and name=" + name + ";")
            elif name != "" and age != "":
                self.cursor.execute("delete from students where id='" + id + "' and age=" + age + " and name='" + name + "';")

        elif name != "":
            if id == "" and age == "":
                self.cursor.execute("delete from students where name='" + name + "';")
            elif id != "" and age == "":
                self.cursor.execute("delete from students where name='" + name + "' and id='" + id + "';")
            elif id == "" and age != "":
                self.cursor.execute("delete from students where name='" + name + "' and age=" + age + ";")

        elif age != "":
            if id == "" and name == "":
                self.cursor.execute("delete from students where age=" + age + ";")
            elif id != "" and name == "":
                self.cursor.execute("delete from students where age=" + age + " and id='" + id + ";")
            elif id == "" and name != "":
                self.cursor.execute("delete from students where age=" + age + " and name='" + name + "';")

        self.db.commit()
        self.clean_inserts()
        self.update_list()

    def b_insertar(self, control):
        id = self.ide.get_text()
        name = self.nome.get_text()
        age = self.idade.get_text()

        self.cursor.execute("select id from students order by id")

        tupla_id = []
        for fila in self.cursor:
            tupla_id.append(int(fila[0]))

        is_ok = False
        is_repead = False
        if id != "":
            for j in tupla_id:
                if j == int(id):
                    is_repead = True
                    break

        if is_repead:
            self.raise_error("Error: ID repetida")
        elif id != "":
            if name == "" and age == "":
                self.raise_error("Error: nombre requerido para la insercion")
            elif name == "" and age != "":
                self.raise_error("Error: nombre requerido para la insercion")
            elif name != "" and age == "":
                self.cursor.execute("insert into students values('" + id + "', '" + name + "', null)")
                is_ok = True
            elif name != "" and age != "":
                self.cursor.execute("insert into students values('" + id + "', '" + name + "', " + age + ")")
                is_ok = True
        else:
            new_id = 1
            for x in tupla_id:
                if x == new_id:
                    new_id += 1
                else:
                    break

            if name != "" and age == "":
                self.cursor.execute("insert into students values('" + str(new_id) + "', '" + name + "', null)")
                is_ok = True
            elif name != "" and age != "":
                self.cursor.execute("insert into students values('" + str(new_id) + "', '" + name + "', " + age + ")")
                is_ok = True
            else:
                self.raise_error("Error: nombre requerido para la inserción")

        self.db.commit()
        if is_ok:
            self.update_list()
            self.clean_inserts()
            self.raise_error()

    def b_buscar(self, control):
        self.raise_error()
        id = self.ide.get_text()
        name = self.nome.get_text()
        age = self.idade.get_text()

        if id != "":
            if name == "" and age == "":
                self.cursor.execute("select * from students where id='" + id + "';")
            elif name == "" and age != "":
                self.cursor.execute("select * from students where id='" + id + "' and age=" + age + ";")
            elif name != "" and age == "":
                self.cursor.execute("select * from students where id='" + id + "' and name=" + name + ";")
            elif name != "" and age != "":
                self.cursor.execute("select * from students where id='" + id + "' and age=" + age + " and name='" + name + "';")

        elif name != "":
            if id == "" and age == "":
                self.cursor.execute("select * from students where name='" + name + "';")
            elif id != "" and age == "":
                self.cursor.execute("select * from students where name='" + name + "' and id='" + id + "';")
            elif id == "" and age != "":
                self.cursor.execute("select * from students where name='" + name + "' and age=" + age + ";")

        elif age != "":
            if id == "" and name == "":
                self.cursor.execute("select * from students where age=" + age + ";")
            elif id != "" and name == "":
                self.cursor.execute("select * from students where age=" + age + " and id='" + id + ";")
            elif id == "" and name != "":
                self.cursor.execute("select * from students where age=" + age + " and name='" + name + "';")

        elif id == "" and age == "" and name == "":
            self.cursor.execute("select * from students order by id")
        else:
            self.raise_error("Error: Búsqueda no contemplada en código")

        lista = Gtk.ListStore(str, str, int)

        for fila in self.cursor:
            lista.append(fila)

        self.view.set_model(lista)
        self.view.show()
        self.clean_inserts()


Panel("Seijas")
Gtk.main()
