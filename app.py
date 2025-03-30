# app.py
import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir los modelos
class DPT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    format_id = db.Column(db.Integer, db.ForeignKey('format_template.id'), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    quality_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class FormatTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    structure = db.Column(db.JSON, nullable=False)

class DPTVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dpt_id = db.Column(db.Integer, db.ForeignKey('dpt.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.JSON, nullable=False)
    change_notes = db.Column(db.String(500))
    updated_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Funciones auxiliares
def evaluate_quality(content):
    return 85.0

def save_to_github(dpt_id, content):
    return True, f"dpts/{dpt_id}.md"

def detect_format(text):
    return 1, 85.0

def extract_components(text):
    return {
        'title': 'Desarrollador Frontend',
        'department': 'Tecnología',
        'summary': 'Responsable del desarrollo de interfaces de usuario web utilizando React y otras tecnologías frontend.'
    }

def suggest_improvements(content):
    return [
        {"campo": "Requisitos", "descripcion": "Añadir requisitos de experiencia específicos (años)"},
        {"campo": "Resumen", "descripcion": "Ampliar el resumen con responsabilidades principales"}
    ]

def convert_to_format(content, source_format_id, target_format_id):
    return {
        'title': content.get('title', ''),
        'department': content.get('department', ''),
        'purpose': content.get('summary', ''),
        'key_responsibilities': 'Diseño de interfaces, investigación de usuarios, prototipado'
    }

# Función para inicializar la base de datos con reintentos
@retry(stop=stop_after_attempt(10), wait=wait_fixed(2), retry=retry_if_exception_type(Exception))
def init_db():
    db.create_all()

# Función para inicializar formatos
# Dentro de app.py, reemplaza la función init_formats() con esta:
def init_formats():
    if FormatTemplate.query.count() == 0:
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
        for format_data in formats:
            format_template = FormatTemplate(
                name=format_data['name'],
                description=format_data['description'],
                structure=format_data['structure']
            )
            db.session.add(format_template)
        db.session.commit()
        app.logger.info("Formatos inicializados.")
    else:
        app.logger.info("Ya existen formatos en la base de datos.")

# Rutas básicas
@app.route('/')
def home():
    return "¡Hola, DPT Manager!"

@app.route('/api/formats', methods=['GET'])
def get_formats():
    formats = FormatTemplate.query.all()
    return {
        'status': 'success',
        'data': [{'id': f.id, 'name': f.name, 'description': f.description, 'structure': f.structure} for f in formats]
    }

@app.route('/api/dpts', methods=['GET'])
def get_dpts():
    department = request.args.get('department')
    query = DPT.query
    if department:
        query = query.filter_by(department=department)
    dpts = query.all()
    return {
        'status': 'success',
        'data': [{'id': d.id, 'title': d.title, 'department': d.department, 'content': d.content} for d in dpts]
    }

@app.route('/api/dpts', methods=['POST'])
def create_dpt():
    data = request.get_json()
    title = data.get('title')
    department = data.get('department')
    format_id = data.get('format_id')
    content = data.get('content')
    created_by = data.get('created_by')

    if not all([title, department, format_id, content, created_by]):
        return jsonify({'status': 'error', 'message': 'Faltan campos requeridos'}), 400

    quality_score = evaluate_quality(content)
    dpt = DPT(
        title=title,
        department=department,
        format_id=format_id,
        content=content,
        created_by=created_by,
        quality_score=quality_score
    )
    db.session.add(dpt)
    db.session.commit()

    # Crear la versión inicial
    version = DPTVersion(
        dpt_id=dpt.id,
        version_number=1,
        content=content,
        updated_by=created_by
    )
    db.session.add(version)
    db.session.commit()

    success, github_path = save_to_github(dpt.id, content)
    if not success:
        return jsonify({'status': 'error', 'message': 'Error al guardar en GitHub'}), 500

    return jsonify({
        'status': 'success',
        'data': {
            'id': dpt.id,
            'title': dpt.title,
            'department': dpt.department,
            'content': dpt.content,
            'quality_score': dpt.quality_score
        }
    }), 201

# Resto de las rutas (update_dpt, analyze_text, convert_format) se mantienen igual...

# Inicializar la base de datos y los formatos dentro de un contexto de aplicación
# Al final de app.py, reemplaza el bloque with app.app_context():
with app.app_context():
    try:
        app.logger.info("Iniciando inicialización de la base de datos...")
        init_db()
        app.logger.info("Base de datos creada con éxito.")
        init_formats()
        app.logger.info("Formatos inicializados con éxito.")
    except Exception as e:
        app.logger.error(f"Error al inicializar la base de datos o formatos: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)