# -*- coding: utf-8 -*-

{
    'name': "Gestión FP",

    'summary': "Gestión de estudiantes y ciclos de FP",

    'description': """
        Gestión Académica de Formación Profesional (FP)
        ===============================================

        Este módulo gestiona el expediente académico de los estudiantes de FP, automatizando el control de progreso y la elegibilidad para prácticas.

        Características Principales:
        ----------------------------
        1. **Gestión de Ciclos y Horas:**
        - Definición de Ciclos Formativos con control de horas totales.
        - Cálculo automático del porcentaje de avance del alumno.

        2. **Lógica de Negocio Automática:**
        - **Regla del 50% (FCT):** El sistema habilita la asignación de empresa de prácticas solo si el alumno ha superado el 50% de las horas.
        - **Regla del 100% (Titulación):** El campo "Nota Media" permanece bloqueado hasta que el alumno completa el 100% de las horas lectivas.

        3. **Interfaz Visual e Inteligente:**
        - **Vista Kanban:** Tarjetas con indicadores visuales de estado (En Curso / FCT / Titulable) y gráfico de progreso.
        - **Vista Lista:** Semáforo de colores para las notas (Suspenso, Aprobado, Notable, Sobresaliente) y barras de avance.
        - **Widgets:** Uso de gráficos circulares (percentpie) y selectores booleanos para una gestión rápida.

        4. **Integridad de Datos:**
        - Validación estricta de formato de correo electrónico.
        - Control de consistencia para evitar registrar más horas aprobadas de las que tiene el ciclo.
            """,

    'author': "Daniel Castelao",
    'website': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/ciclo_fp_views.xml",
        "views/estudiante_fp_views.xml",
        "views/menu.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}

