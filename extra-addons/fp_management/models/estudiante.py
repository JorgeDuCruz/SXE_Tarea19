# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError

class Estudiante(models.Model):
    _name = "fp_management.estudiante"
    _description = "Estudiante de FP"
    _order = "name asc"

    name = fields.Char(string="Nombre del Estudiante", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    edad = fields.Integer(string="Edad",compute="_compute_edad")
    email = fields.Char(string="Email")
    ciclo_id = fields.Many2one("fp_management.ciclo", string="Ciclo Formativo", required=True)


    horas_aprobadas = fields.Integer(string="Horas aprobadas")
    horas_ciclo = fields.Integer(string="Horas totales del ciclo",related=ciclo_id.horas_totales,readonly = True)
    nota_media = fields.Float(string="Nota media")
    porcentaje_aprobadas = fields.Float(string="% Aprobado",compute="_compute_datos_academicos")
    permite_fct = fields.Boolean(string = "Tiene fct permitida",compute="_compute_datos_academicos")
    
    via_acceso = fields.Selection(
        [
            ("eso", "ESO"),
            ("ciclo_medio", "Ciclo Medio"),
            ("bachillerato", "Bachillerato"),
            ("prueba_acceso", "Prueba de Acceso"),
            ("otros", "Otros"),
        ],
        string="Vía de Acceso",
        required=True,
        default="eso",
    )

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for record in self:
            if record.fecha_nacimiento:
                hoy = date.today()
                diferencia = relativedelta(hoy,record.fecha_nacimiento)
                record.edad = diferencia.years
            else:
                record.edad = 0

    @api.depends('horas_aprobadas','horas_ciclo')
    def _compute_datos_academicos(self):
        for record in self:
            if record.horas_ciclo > 0:
                calculo = record.horas_aprobadas/record.horas_ciclo * 100

                record.porcentaje_aprobadas = min(calculo,100.0)
                record.permite_fct = calculo>=50
            else:
                record.porcentaje_aprobadas = 0.0
                record.permite_fct=False

    @api.constrains('email')
    def check_mail(self):
        # Expresión regular estándar para emails
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("El formato del correo electrónico no es válido. Debe ser tipo 'ejemplo@correo.com'")





