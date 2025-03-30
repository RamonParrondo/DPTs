import os
import sys
import json
import pytest
from unittest import mock
from datetime import datetime

# Asegurarse de que el directorio del proyecto esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importar la aplicación Flask
from app import app, db, DPT, FormatTemplate, DPTVersion

@pytest.fixture
def client():
    """Configurar cliente de prueba"""
    # Configurar la aplicación para pruebas
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Crear contexto de aplicación
    with app.app_context():
        # Crear tablas en la base de datos
        db.create_all()
        
        # Crear formatos de prueba
        format1 = FormatTemplate(
            name='Formato de Prueba 1',
            description='Formato para pruebas unitarias',
            structure={
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'summary': {'type': 'textarea', 'required': True, 'label': 'Resumen del Puesto'}
            }
        )
        db.session.add(format1)
        db.session.commit()
        
    # Crear un cliente de prueba
    with app.test_client() as client:
        yield client
    
    # Limpiar después de las pruebas
    with app.app_context():
        db.drop_all()

def test_get_formats(client):
    """Probar la obtención de formatos"""
    response = client.get('/api/formats')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['name'] == 'Formato de Prueba 1'

def test_create_dpt(client):
    """Probar la creación de un DPT"""
    # Datos de prueba
    test_data = {
        'title': 'Desarrollador Python',
        'department': 'Tecnología',
        'format_id': 1,
        'content': {
            'title': 'Desarrollador Python',
            'department': 'Tecnología',
            'summary': 'Responsable del desarrollo de aplicaciones en Python'
        },
        'created_by': 'test_user'
    }

    # Simular la evaluación de calidad
    with mock.patch('app.evaluate_quality', return_value=85.0):
        # Simular el guardado en GitHub
        with mock.patch('app.save_to_github', return_value=(True, 'dpts/test.md')):
            response = client.post('/api/dpts',
                                   data=json.dumps(test_data),
                                   content_type='application/json')

    data = json.loads(response.data)
    print("Respuesta de la API:", data)  # Agregar esta línea para depurar

    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['title'] == 'Desarrollador Python'
    assert data['quality_score'] == 85.0

def test_get_dpts(client):
    """Probar la obtención de DPTs"""
    # Crear un DPT de prueba
    with app.app_context():
        dpt = DPT(
            title='Analista de Datos',
            department='Business Intelligence',
            format_id=1,
            content={
                'title': 'Analista de Datos',
                'department': 'Business Intelligence',
                'summary': 'Análisis de datos para toma de decisiones'
            },
            created_by='test_user',
            status='active',
            quality_score=78.5
        )
        db.session.add(dpt)
        db.session.commit()
    
    # Obtener todos los DPTs
    response = client.get('/api/dpts')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['title'] == 'Analista de Datos'
    
    # Probar filtrado por departamento
    response = client.get('/api/dpts?department=Business%20Intelligence')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['data']) == 1
    
    # Probar filtrado por departamento inexistente
    response = client.get('/api/dpts?department=Marketing')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['data']) == 0

def test_update_dpt(client):
    """Probar la actualización de un DPT"""
    # Crear un DPT de prueba
    with app.app_context():
        dpt = DPT(
            title='Gerente de Proyectos',
            department='PMO',
            format_id=1,
            content={
                'title': 'Gerente de Proyectos',
                'department': 'PMO',
                'summary': 'Gestión de proyectos de tecnología'
            },
            created_by='test_user',
            status='active',
            quality_score=80.0
        )
        db.session.add(dpt)
        db.session.commit()
        dpt_id = dpt.id
    
    # Datos para actualizar
    update_data = {
        'title': 'Gerente de Proyectos Senior',
        'content': {
            'title': 'Gerente de Proyectos Senior',
            'department': 'PMO',
            'summary': 'Gestión de proyectos de tecnología de alta complejidad'
        },
        'updated_by': 'test_admin',
        'change_notes': 'Actualización de título y resumen'
    }
    
    # Simular la evaluación de calidad
    with mock.patch('app.evaluate_quality', return_value=88.0):
        # Simular el guardado en GitHub
        with mock.patch('app.save_to_github', return_value=(True, 'dpts/test.md')):
            response = client.put(f'/api/dpts/{dpt_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
    
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['title'] == 'Gerente de Proyectos Senior'
    
    # Verificar los cambios en la base de datos
    with app.app_context():
        updated_dpt = DPT.query.get(dpt_id)
        assert updated_dpt.title == 'Gerente de Proyectos Senior'
        assert updated_dpt.quality_score == 88.0
        
        # Verificar que se creó una nueva versión
        versions = DPTVersion.query.filter_by(dpt_id=dpt_id).all()
        assert len(versions) == 1  # Solo se creó la versión de la actualización
        assert versions[0].change_notes == 'Actualización de título y resumen'

def test_analyze_text(client):
    """Probar el análisis de texto de DPT"""
    # Texto de prueba
    test_text = """
    Título del Puesto: Desarrollador Frontend
    
    Departamento: Tecnología
    
    Resumen del Puesto:
    Responsable del desarrollo de interfaces de usuario web utilizando React y otras tecnologías frontend.
    
    Requisitos:
    - Experiencia con React, HTML5, CSS3 y JavaScript
    - Conocimientos de UX/UI
    - Capacidad para trabajar en equipo
    """
    
    # Datos para la solicitud
    request_data = {
        'text': test_text,
        'options': {
            'identify_format': True,
            'extract_components': True,
            'quality_check': True,
            'suggest_improvements': True
        }
    }
    
    # Simular funciones de análisis
    with mock.patch('app.detect_format', return_value=(1, 85.0)):
        with mock.patch('app.extract_components', return_value={
            'title': 'Desarrollador Frontend',
            'department': 'Tecnología',
            'summary': 'Responsable del desarrollo de interfaces de usuario web utilizando React y otras tecnologías frontend.'
        }):
            with mock.patch('app.evaluate_quality', return_value=75.0):
                with mock.patch('app.suggest_improvements', return_value=[
                    {"campo": "Requisitos", "descripcion": "Añadir requisitos de experiencia específicos (años)"},
                    {"campo": "Resumen", "descripcion": "Ampliar el resumen con responsabilidades principales"}
                ]):
                    response = client.post('/api/analyze/text',
                                          data=json.dumps(request_data),
                                          content_type='application/json')
    
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert 'format' in data['data']
    assert 'components' in data['data']
    assert 'quality' in data['data']
    assert 'suggestions' in data['data']
    assert data['data']['format']['id'] == 1
    assert data['data']['components']['title'] == 'Desarrollador Frontend'
    assert data['data']['quality']['overall_score'] == 75.0
    assert len(data['data']['suggestions']) == 2

def test_convert_format(client):
    """Probar la conversión entre formatos"""
    # Crear un formato adicional para la conversión
    with app.app_context():
        format2 = FormatTemplate(
            name='Formato de Prueba 2',
            description='Segundo formato para pruebas',
            structure={
                'title': {'type': 'text', 'required': True, 'label': 'Título del Puesto'},
                'department': {'type': 'text', 'required': True, 'label': 'Departamento'},
                'purpose': {'type': 'textarea', 'required': True, 'label': 'Propósito del Puesto'},
                'key_responsibilities': {'type': 'textarea', 'required': True, 'label': 'Responsabilidades Clave'}
            }
        )
        db.session.add(format2)
        db.session.commit()
    
    # Datos del DPT original
    original_content = {
        'title': 'Diseñador UX',
        'department': 'Diseño',
        'summary': 'Crear experiencias de usuario intuitivas y atractivas'
    }
    
    # Datos de solicitud
    request_data = {
        'content': original_content,
        'source_format_id': 1,
        'target_format_id': 2
    }
    
    # Contenido convertido esperado
    converted_content = {
        'title': 'Diseñador UX',
        'department': 'Diseño',
        'purpose': 'Crear experiencias de usuario intuitivas y atractivas',
        'key_responsibilities': 'Diseño de interfaces, investigación de usuarios, prototipado'
    }
    
    # Simular la conversión
    with mock.patch('app.convert_to_format', return_value=converted_content):
        response = client.post('/api/convert',
                              data=json.dumps(request_data),
                              content_type='application/json')
    
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['source_format_id'] == 1
    assert data['data']['target_format_id'] == 2
    assert data['data']['converted_content'] == converted_content

if __name__ == '__main__':
    pytest.main(['-v'])
