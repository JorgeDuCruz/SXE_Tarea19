# -*- coding: utf-8 -*-

from odoo import models, fields

class Ciclo(models.Model):
    _name = "fp_gestion.ciclo"
    _description = "Ciclo Formativo de FP"

    name = fields.Char(string="Nombre del Ciclo", required=True)
    descripcion = fields.Text(string="Descripción del ciclo formativo")
    horas_totales = fields.Integer(string="Horas Totales", help="Número total de horas lectivas del ciclo. Es fundamental para calcular el porcentaje de progreso de los alumnos.", default=600)
    
    estudiante_ids = fields.One2many("fp_gestion.estudiante", "ciclo_id", string="Estudiantes")
