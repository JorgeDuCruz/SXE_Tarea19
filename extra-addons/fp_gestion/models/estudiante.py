# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError 
from dateutil.relativedelta import relativedelta
import re

class Estudiante(models.Model):
    _name = "fp_gestion.estudiante"
    _description = "Estudiante de FP"
    _order = "name asc"
    
    name = fields.Char(string="Nombre del Estudiante", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    edad = fields.Integer(string="Edad", compute="_compute_edad", help="Calculada automáticamente basada en la fecha de nacimiento.")
    email = fields.Char(string="Correo Electrónico") 
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
    
    ciclo_id = fields.Many2one("fp_gestion.ciclo", string="Ciclo Formativo", required=True)
    horas_ciclo = fields.Integer(string="Horas del Ciclo", related="ciclo_id.horas_totales", help="Total de horas lectivas definidas en la ficha del Ciclo Formativo.", readonly=True)
    horas_aprobadas = fields.Integer(string="Horas Aprobadas", help="Introduce aquí cuántas horas ha superado el alumno hasta el momento.")
    porcentaje_aprobadas = fields.Float(string="% Aprobado", compute="_compute_datos_academicos", help="Porcentaje de Horas Aprobadas / Horas Totales", store=True)

    permite_fct = fields.Boolean(string="Apto para FCT", compute="_compute_datos_academicos", help="Se marca automáticamente si el alumno ha superado el 50% del ciclo.", store=True)
    empresa_fct = fields.Char(string="Empresa de Prácticas")
    
    nota_media = fields.Float(string="Nota Media", help="La nota media solo se puede introducir cuando el alumno ha completado el 100% de las horas.", default=0.0)

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for record in self:
            if record.fecha_nacimiento:
                hoy = date.today()
                diferencia = relativedelta(hoy, record.fecha_nacimiento)
                record.edad = diferencia.years
            else:
                record.edad = 0

    @api.depends('horas_aprobadas', 'ciclo_id.horas_totales')
    def _compute_datos_academicos(self):
        for record in self:
            total_horas = record.ciclo_id.horas_totales
            
            if total_horas > 0:
                calculo = (record.horas_aprobadas / total_horas) * 100
                
                record.porcentaje_aprobadas = min(calculo, 100.0)
                record.permite_fct = calculo >= 50
            else:
                record.porcentaje_aprobadas = 0.0
                record.permite_fct = False

    @api.constrains('nota_media')
    def _check_nota_media(self):
        for record in self:
            if record.nota_media < 0 or record.nota_media > 10:
                raise ValidationError("La nota media debe estar entre 0 y 10.")

    @api.constrains('horas_aprobadas', 'ciclo_id')
    def _check_horas_validas(self):
        for record in self:
            if record.horas_aprobadas < 0:
                 raise ValidationError("Las horas aprobadas no pueden ser negativas.")
            
            if record.ciclo_id and record.horas_aprobadas > record.ciclo_id.horas_totales:
                 raise ValidationError(
                     f"Error: Has introducido {record.horas_aprobadas} horas, pero el ciclo "
                     f"{record.ciclo_id.name} solo tiene {record.ciclo_id.horas_totales} horas."
                 )
                 
    @api.constrains('email')
    def _check_email(self):
        # Expresión regular estándar para emails
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        
        for record in self:
            # Solo validamos si el campo tiene algo escrito
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("El formato del correo electrónico no es válido. Debe ser tipo 'ejemplo@correo.com'")