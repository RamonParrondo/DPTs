"""
Script para inicializar los 10 formatos de DPT en la base de datos.
Este script debe ejecutarse una sola vez para configurar el sistema.
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurar la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dpt_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importar el modelo FormatTemplate
class FormatTemplate(db.Model):
    """Modelo para almacenar plantillas de formatos de DPT"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    structure = db.Column(db.JSON, nullable=False)  # Estructura de campos
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

def init_formats():
    """Inicializar los 10 formatos de DPT"""
    
    # Verificar si ya existen formatos
    existing_count = FormatTemplate.query.count()
    if existing_count > 0:
        print(f"Ya existen {existing_count} formatos en la base de datos.")
        if input("¿Desea sobrescribirlos? (s/n): ").lower() != 's':
            print("Operación cancelada.")
            return
        else:
            # Eliminar formatos existentes
            FormatTemplate.query.delete()
            db.session.commit()
    
    # Definir los 10 formatos de DPT
    formats = [
        # Formato 1: Estándar Básico
        {
            'name': 'Formato 1: Estándar Básico',
            'description': 'Formato básico con campos esenciales para cualquier puesto',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'summary': {'type': 'textarea', 'required': True, 'label': 'Resumen del Puesto'},
                'responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Principales'},
                'qualifications': {'type': 'textarea', 'required': True, 'label': 'Requisitos y Cualificaciones'},
                'reports_to': {'type': 'text', 'required': True, 'label': 'Reporta a'},
                'supervises': {'type': 'text', 'required': False, 'label': 'Supervisa a'},
                'working_conditions': {'type': 'textarea', 'required': False, 'label': 'Condiciones de Trabajo'}
            }
        },
        
        # Formato 2: Detallado por Competencias
        {
            'name': 'Formato 2: Detallado por Competencias',
            'description': 'Formato que enfatiza las competencias y habilidades requeridas',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'purpose': {'type': 'textarea', 'required': True, 'label': 'Propósito del Puesto'},
                'key_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Clave'},
                'technical_skills': {'type': 'textarea', 'required': True, 'label': 'Habilidades Técnicas'},
                'soft_skills': {'type': 'textarea', 'required': True, 'label': 'Habilidades Blandas'},
                'leadership_competencies': {'type': 'textarea', 'required': False, 'label': 'Competencias de Liderazgo'},
                'education': {'type': 'textarea', 'required': True, 'label': 'Formación Académica'},
                'experience': {'type': 'textarea', 'required': True, 'label': 'Experiencia'},
                'reporting_line': {'type': 'text', 'required': True, 'label': 'Línea de Reporte'},
                'direct_reports': {'type': 'text', 'required': False, 'label': 'Reportes Directos'},
                'key_interactions': {'type': 'textarea', 'required': True, 'label': 'Interacciones Clave'}
            }
        },
        
        # Formato 3: Por Objetivos
        {
            'name': 'Formato 3: Por Objetivos',
            'description': 'Enfocado en objetivos y metas específicas del puesto',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'mission': {'type': 'textarea', 'required': True, 'label': 'Misión del Puesto'},
                'key_objectives': {'type': 'textarea', 'required': True, 'label': 'Objetivos Clave'},
                'performance_indicators': {'type': 'textarea', 'required': True, 'label': 'Indicadores de Desempeño'},
                'qualifications': {'type': 'textarea', 'required': True, 'label': 'Cualificaciones'},
                'reports_to': {'type': 'text', 'required': True, 'label': 'Reporta a'},
                'relationships': {'type': 'textarea', 'required': True, 'label': 'Relaciones Clave'}
            }
        },
        
        # Formato 4: Enfoque en Resultados
        {
            'name': 'Formato 4: Enfoque en Resultados',
            'description': 'Centrado en los resultados esperados y el impacto del puesto',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'position_summary': {'type': 'textarea', 'required': True, 'label': 'Resumen del Puesto'},
                'key_result_areas': {'type': 'textarea', 'required': True, 'label': 'Áreas de Resultado Clave'},
                'success_metrics': {'type': 'textarea', 'required': True, 'label': 'Métricas de Éxito'},
                'primary_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Primarias'},
                'decision_making_authority': {'type': 'textarea', 'required': True, 'label': 'Autoridad de Toma de Decisiones'},
                'qualifications': {'type': 'textarea', 'required': True, 'label': 'Cualificaciones'},
                'organizational_relationships': {'type': 'textarea', 'required': True, 'label': 'Relaciones Organizacionales'}
            }
        },
        
        # Formato 5: Detalle Técnico
        {
            'name': 'Formato 5: Detalle Técnico',
            'description': 'Orientado a roles técnicos con énfasis en habilidades específicas',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'role_overview': {'type': 'textarea', 'required': True, 'label': 'Visión General del Rol'},
                'technical_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Técnicas'},
                'technical_requirements': {'type': 'textarea', 'required': True, 'label': 'Requisitos Técnicos'},
                'tools_technologies': {'type': 'textarea', 'required': True, 'label': 'Herramientas y Tecnologías'},
                'certifications': {'type': 'textarea', 'required': False, 'label': 'Certificaciones'},
                'problem_solving': {'type': 'textarea', 'required': True, 'label': 'Resolución de Problemas'},
                'education_experience': {'type': 'textarea', 'required': True, 'label': 'Educación y Experiencia'},
                'reporting_structure': {'type': 'text', 'required': True, 'label': 'Estructura de Reporte'},
                'collaboration': {'type': 'textarea', 'required': True, 'label': 'Colaboración'}
            }
        },
        
        # Formato 6: Ejecutivo
        {
            'name': 'Formato 6: Ejecutivo',
            'description': 'Diseñado para roles de liderazgo y dirección ejecutiva',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'position_purpose': {'type': 'textarea', 'required': True, 'label': 'Propósito del Puesto'},
                'scope_of_position': {'type': 'textarea', 'required': True, 'label': 'Alcance del Puesto'},
                'strategic_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Estratégicas'},
                'operational_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Operativas'},
                'leadership_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades de Liderazgo'},
                'decision_authority': {'type': 'textarea', 'required': True, 'label': 'Autoridad de Decisión'},
                'experience_qualifications': {'type': 'textarea', 'required': True, 'label': 'Experiencia y Cualificaciones'},
                'leadership_competencies': {'type': 'textarea', 'required': True, 'label': 'Competencias de Liderazgo'},
                'key_relationships': {'type': 'textarea', 'required': True, 'label': 'Relaciones Clave'},
                'performance_measures': {'type': 'textarea', 'required': True, 'label': 'Medidas de Desempeño'}
            }
        },
        
        # Formato 7: Funcional Avanzado
        {
            'name': 'Formato 7: Funcional Avanzado',
            'description': 'Descripción detallada y estructurada con actividades y porcentajes de tiempo',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'position_summary': {'type': 'textarea', 'required': True, 'label': 'Resumen del Puesto'},
                'essential_functions': {'type': 'textarea', 'required': True, 'label': 'Funciones Esenciales'},
                'time_allocation': {'type': 'textarea', 'required': True, 'label': 'Asignación de Tiempo (%)'},
                'daily_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Diarias'},
                'weekly_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Semanales'},
                'monthly_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Mensuales'},
                'quarterly_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Trimestrales'},
                'qualifications': {'type': 'textarea', 'required': True, 'label': 'Cualificaciones'},
                'physical_requirements': {'type': 'textarea', 'required': False, 'label': 'Requisitos Físicos'},
                'work_environment': {'type': 'textarea', 'required': False, 'label': 'Entorno de Trabajo'},
                'reporting_relationship': {'type': 'text', 'required': True, 'label': 'Relación de Reporte'}
            }
        },
        
        # Formato 8: Académico/Investigación
        {
            'name': 'Formato 8: Académico/Investigación',
            'description': 'Orientado a roles académicos o de investigación',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento/Facultad'},
                'position_overview': {'type': 'textarea', 'required': True, 'label': 'Visión General del Puesto'},
                'research_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades de Investigación'},
                'teaching_responsibilities': {'type': 'textarea', 'required': False, 'label': 'Responsabilidades de Enseñanza'},
                'administrative_duties': {'type': 'textarea', 'required': False, 'label': 'Deberes Administrativos'},
                'publication_expectations': {'type': 'textarea', 'required': False, 'label': 'Expectativas de Publicación'},
                'grant_funding': {'type': 'textarea', 'required': False, 'label': 'Financiación y Subvenciones'},
                'academic_qualifications': {'type': 'textarea', 'required': True, 'label': 'Cualificaciones Académicas'},
                'research_experience': {'type': 'textarea', 'required': True, 'label': 'Experiencia en Investigación'},
                'specialized_knowledge': {'type': 'textarea', 'required': True, 'label': 'Conocimiento Especializado'},
                'reporting_relationship': {'type': 'text', 'required': True, 'label': 'Relación de Reporte'},
                'collaboration_networks': {'type': 'textarea', 'required': False, 'label': 'Redes de Colaboración'}
            }
        },
        
        # Formato 9: Sector Público
        {
            'name': 'Formato 9: Sector Público',
            'description': 'Adaptado a los requisitos y estructura del sector público',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Denominación del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Unidad Administrativa'},
                'position_code': {'type': 'text', 'required': True, 'label': 'Código del Puesto'},
                'job_level': {'type': 'text', 'required': True, 'label': 'Nivel del Puesto'},
                'mission': {'type': 'textarea', 'required': True, 'label': 'Misión del Puesto'},
                'key_functions': {'type': 'textarea', 'required': True, 'label': 'Funciones Principales'},
                'legal_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Legales'},
                'requirements': {'type': 'textarea', 'required': True, 'label': 'Requisitos'},
                'formal_education': {'type': 'textarea', 'required': True, 'label': 'Formación Académica'},
                'additional_knowledge': {'type': 'textarea', 'required': True, 'label': 'Conocimientos Adicionales'},
                'experience': {'type': 'textarea', 'required': True, 'label': 'Experiencia'},
                'competencies': {'type': 'textarea', 'required': True, 'label': 'Competencias'},
                'hierarchical_relationship': {'type': 'textarea', 'required': True, 'label': 'Relación Jerárquica'},
                'special_conditions': {'type': 'textarea', 'required': False, 'label': 'Condiciones Especiales'}
            }
        },
        
        # Formato 10: Internacional/Multinacional
        {
            'name': 'Formato 10: Internacional/Multinacional',
            'description': 'Diseñado para roles en entornos internacionales o multinacionales',
            'structure': {
                'title': {'type': 'text', 'required': True, 'label': 'Job Title / Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Department / Departamento'},
                'location': {'type': 'text', 'required': True, 'label': 'Location / Ubicación'},
                'region': {'type': 'text', 'required': True, 'label': 'Region / Región'},
                'job_purpose': {'type': 'textarea', 'required': True, 'label': 'Job Purpose / Propósito del Puesto'},
                'key_accountabilities': {'type': 'textarea', 'required': True, 'label': 'Key Accountabilities / Responsabilidades Clave'},
                'global_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Global Responsibilities / Responsabilidades Globales'},
                'local_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Local Responsibilities / Responsabilidades Locales'},
                'cross_cultural_competencies': {'type': 'textarea', 'required': True, 'label': 'Cross-Cultural Competencies / Competencias Interculturales'},
                'language_requirements': {'type': 'textarea', 'required': True, 'label': 'Language Requirements / Requisitos de Idioma'},
                'education': {'type': 'textarea', 'required': True, 'label': 'Education / Formación Académica'},
                'experience': {'type': 'textarea', 'required': True, 'label': 'Experience / Experiencia'},
                'travel_requirements': {'type': 'textarea', 'required': True, 'label': 'Travel Requirements / Requisitos de Viaje'},
                'reporting_line': {'type': 'textarea', 'required': True, 'label': 'Reporting Line / Línea de Reporte'},
                'matrix_relationships': {'type': 'textarea', 'required': True, 'label': 'Matrix Relationships / Relaciones Matriciales'}
            }
        }
    ]
    
    # Insertar formatos en la base de datos
    for format_data in formats:
        format_template = FormatTemplate(
            name=format_data['name'],
            description=format_data['description'],
            structure=format_data['structure']
        )
        db.session.add(format_template)
    
    db.session.commit()
    print(f"Se han inicializado {len(formats)} formatos de DPT correctamente.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Asegurar que la tabla existe
        init_formats()
