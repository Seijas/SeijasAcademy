#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import sqlite3 as dbapi
from panel import Panel

__author__ = 'Seijas'


class Login:

    db = dbapi.connect("database.db")
    cursor = db.cursor()

    def __init__(self):
        file = "./views/login.glade"
        builder = Gtk.Builder()
        builder.add_from_file(file)

        signals = {
            "button_login": self.button_login,
            "on_login_destroy": Gtk.main_quit
        }

        builder.connect_signals(signals)

        self.user = builder.get_object("entry_user")
        self.password = builder.get_object("entry_pass")
        self.button_login = builder.get_object("button_login")
        self.window = builder.get_object("window_login")
        self.error = builder.get_object("label_error")

    def button_login(self, control):
        self.error.set_text("")
        user = self.user.get_text()
        password = self.password.get_text()

        self.cursor.execute("select * from users where name='" + user + "';")
        for result in self.cursor:
            if result[1] == password:
                self.window.set_visible(False)
                Panel(user)
            else:
                self.error.set_text("Datos Incorrectos")
        self.error.set_text("Usuario no encontrado")

Login()
Gtk.main()
