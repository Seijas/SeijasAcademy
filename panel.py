#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

__author__ = 'Seijas'

from gi.repository import Gtk
import sqlite3 as dbapi


class Panel:

    db = dbapi.connect("database.db")
    cursor = db.cursor()

    def __init__(self):
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

        render = Gtk.CellRendererText()

        columna1 = Gtk.TreeViewColumn("ID", render, text=0)
        columna2 = Gtk.TreeViewColumn("Nombre", render, text=1)
        columna3 = Gtk.TreeViewColumn("Edad", render, text=2)

        self.view.append_column(columna1)
        self.view.append_column(columna2)
        self.view.append_column(columna3)

        self.update_list()

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
