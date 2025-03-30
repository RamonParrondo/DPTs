        Analiza la siguiente Descripción de Puesto de Trabajo y sugiere mejoras concretas.
        
        {quality_info}
        
        Enfócate en:
        1. Campos incompletos o con poca información
        2. Claridad de la redacción
        3. Especificidad de responsabilidades y requisitos
        4. Inclusión de métricas o indicadores medibles
        5. Coherencia general del documento
        
        Proporciona al menos 3 sugerencias de mejora concretas y aplicables.
        Responde solo con un array JSON de sugerencias, donde cada sugerencia tenga un campo y una descripción.
        
        Descripción de Puesto:
        {content_text}
        """
        
        response = model.generate_content(prompt)
        
        # Extraer JSON de la respuesta
        match = re.search(r'```json\s*(.*?)\s*```', response.text, re.DOTALL)
        json_str = match.group(1) if match else response.text
        
        suggestions = json.loads(json_str)
        return suggestions
    
    except Exception as e:
        print(f"Error al generar sugerencias con IA: {e}")
        # Sugerencias generales si falla la IA
        return [
            {"campo": "General", "descripcion": "Añadir más detalles específicos sobre las responsabilidades principales."},
            {"campo": "Requisitos", "descripcion": "Especificar niveles de experiencia y formación requeridos."},
            {"campo": "Métricas", "descripcion": "Incluir indicadores medibles para evaluar el desempeño."}
        ]

def convert_to_format(dpt_content, source_format_id, target_format_id):
    """
    Convierte un DPT de un formato a otro
    """
    source_format = FormatTemplate.query.get(source_format_id)
    target_format = FormatTemplate.query.get(target_format_id)
    
    if not source_format or not target_format:
        return {}
    
    # Preparar contenido para la conversión
    content_text = "\n\n".join([f"{source_format.structure[k]['label']}:\n{v}" for k, v in dpt_content.items() if v])
    
    # Campos objetivo
    target_fields = [{"field": field, "label": info["label"]} for field, info in target_format.structure.items()]
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Necesito convertir una Descripción de Puesto de Trabajo del formato "{source_format.name}" 
        al formato "{target_format.name}".
        
        A continuación está el contenido actual:
        
        {content_text}
        
        Necesito que lo reestructures para el formato destino que tiene estos campos:
        {json.dumps(target_fields)}
        
        Devuelve solo un JSON donde las claves sean los nombres de los campos y los valores sean el contenido 
        para cada campo. Asegúrate de preservar toda la información importante y adaptarla a la nueva estructura.
        """
        
        response = model.generate_content(prompt)
        
        # Extraer JSON de la respuesta
        match = re.search(r'```json\s*(.*?)\s*```', response.text, re.DOTALL)
        json_str = match.group(1) if match else response.text
        
        converted_content = json.loads(json_str)
        return converted_content
    
    except Exception as e:
        print(f"Error en la conversión de formato con IA: {e}")
        
        # Si falla la IA, intentar mapeo manual básico
        converted_content = {}
        
        # Mapeo de campos comunes
        common_field_mappings = {
            "title": ["title", "job_title", "position_title"],
            "department": ["department", "business_unit", "area"],
            "summary": ["summary", "purpose", "mission", "job_summary", "description"],
            "responsibilities": ["responsibilities", "key_responsibilities", "duties", "functions", "key_duties"],
            "qualifications": ["qualifications", "requirements", "skills", "technical_skills", "competencies"],
            "reports_to": ["reports_to", "supervisor", "reporting_line", "manager"],
        }
        
        # Para cada campo en el formato destino
        for target_field in target_format.structure.keys():
            # Buscar en campos directamente equivalentes
            if target_field in dpt_content and dpt_content[target_field]:
                converted_content[target_field] = dpt_content[target_field]
                continue
                
            # Buscar en mapeos de campos comunes
            if target_field in common_field_mappings:
                for source_field in common_field_mappings[target_field]:
                    if source_field in dpt_content and dpt_content[source_field]:
                        converted_content[target_field] = dpt_content[source_field]
                        break
                        
            # Si aún no se ha encontrado contenido, dejar en blanco
            if target_field not in converted_content:
                converted_content[target_field] = ""
                
        return converted_content

def save_to_github(dpt):
    """
    Guarda el DPT en un repositorio de GitHub
    """
    try:
        repo = github_client.get_repo(GITHUB_REPO)
        
        # Convertir DPT a markdown
        format_template = FormatTemplate.query.get(dpt.format_id)
        content_md = f"# {dpt.title}\n\n"
        content_md += f"**Departamento:** {dpt.department}\n\n"
        
        for field, value in dpt.content.items():
            if value and field in format_template.structure:
                content_md += f"## {format_template.structure[field]['label']}\n\n"
                content_md += f"{value}\n\n"
        
        # Metadata
        content_md += f"---\n\n"
        content_md += f"**ID:** {dpt.id}\n\n"
        content_md += f"**Formato:** {format_template.name}\n\n"
        content_md += f"**Fecha de creación:** {dpt.created_at.strftime('%Y-%m-%d')}\n\n"
        content_md += f"**Última actualización:** {dpt.updated_at.strftime('%Y-%m-%d')}\n\n"
        
        # Crear o actualizar archivo en GitHub
        file_path = f"dpts/{dpt.id}.md"
        message = f"Update DPT: {dpt.title}"
        
        # Verificar si el archivo ya existe
        try:
            content = repo.get_contents(file_path)
            repo.update_file(file_path, message, content_md, content.sha)
        except:
            # Si no existe, crear nuevo
            repo.create_file(file_path, message, content_md)
            
        return True, file_path
        
    except Exception as e:
        print(f"Error al guardar en GitHub: {e}")
        return False, str(e)

def generate_dpt_report(dpt_ids=None):
    """
    Genera un informe con todos los DPTs o con los especificados
    """
    try:
        if dpt_ids:
            dpts = DPT.query.filter(DPT.id.in_(dpt_ids)).all()
        else:
            dpts = DPT.query.filter_by(status='active').all()
            
        # Crear el informe en markdown
        report_md = "# Informe de Descripciones de Puesto de Trabajo\n\n"
        report_md += f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        report_md += f"Total de DPTs: {len(dpts)}\n\n"
        
        # Tabla resumen
        report_md += "## Resumen de DPTs\n\n"
        report_md += "| ID | Título | Departamento | Formato | Última Actualización |\n"
        report_md += "|---|--------|-------------|---------|----------------------|\n"
        
        for dpt in dpts:
            format_name = FormatTemplate.query.get(dpt.format_id).name if dpt.format_id else "Desconocido"
            report_md += f"| {dpt.id} | {dpt.title} | {dpt.department} | {format_name} | {dpt.updated_at.strftime('%Y-%m-%d')} |\n"
            
        # Detalles de cada DPT
        report_md += "\n## Detalles de DPTs\n\n"
        
        for dpt in dpts:
            report_md += f"### {dpt.title}\n\n"
            report_md += f"**ID:** {dpt.id}  \n"
            report_md += f"**Departamento:** {dpt.department}  \n"
            format_name = FormatTemplate.query.get(dpt.format_id).name if dpt.format_id else "Desconocido"
            report_md += f"**Formato:** {format_name}  \n"
            report_md += f"**Fecha de creación:** {dpt.created_at.strftime('%Y-%m-%d')}  \n"
            report_md += f"**Última actualización:** {dpt.updated_at.strftime('%Y-%m-%d')}  \n"
            if dpt.quality_score:
                report_md += f"**Puntuación de calidad:** {dpt.quality_score:.1f}/100  \n"
            
            report_md += "\n"
            
            # Contenido del DPT
            format_template = FormatTemplate.query.get(dpt.format_id)
            if format_template:
                for field, value in dpt.content.items():
                    if value and field in format_template.structure:
                        report_md += f"#### {format_template.structure[field]['label']}\n\n"
                        report_md += f"{value}\n\n"
            
            report_md += "---\n\n"
        
        # Generar archivo
        report_path = f"reports/dpt_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        os.makedirs("reports", exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
            
        # Opcionalmente, convertir a HTML o PDF
        html_report = markdown2.markdown(report_md, extras=["tables", "header-ids"])
        html_path = report_path.replace('.md', '.html')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Informe de DPTs</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    h1, h2, h3, h4 {{ color: #333; }}
                    hr {{ border: 0; border-top: 1px solid #eee; margin: 30px 0; }}
                </style>
            </head>
            <body>
                {html_report}
            </body>
            </html>
            """)
            
        return True, html_path
        
    except Exception as e:
        print(f"Error al generar informe: {e}")
        return False, str(e)

# Rutas de la API

@app.route('/api/formats', methods=['GET'])
def get_formats():
    """Obtener todos los formatos disponibles"""
    formats = FormatTemplate.query.filter_by(is_active=True).all()
    return jsonify({
        'status': 'success',
        'data': [{
            'id': f.id,
            'name': f.name,
            'description': f.description,
            'structure': f.structure
        } for f in formats]
    })

@app.route('/api/formats/<int:format_id>', methods=['GET'])
def get_format(format_id):
    """Obtener un formato específico"""
    format_template = FormatTemplate.query.get_or_404(format_id)
    return jsonify({
        'status': 'success',
        'data': {
            'id': format_template.id,
            'name': format_template.name,
            'description': format_template.description,
            'structure': format_template.structure
        }
    })

@app.route('/api/dpts', methods=['GET'])
def get_dpts():
    """Obtener todos los DPTs con filtros opcionales"""
    # Parámetros de filtrado
    department = request.args.get('department')
    status = request.args.get('status', 'active')
    search = request.args.get('search')
    
    query = DPT.query
    
    if department:
        query = query.filter_by(department=department)
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(
            (DPT.title.contains(search)) | 
            (DPT.department.contains(search)) |
            (DPT.id.contains(search))
        )
        
    dpts = query.order_by(DPT.updated_at.desc()).all()
    
    return jsonify({
        'status': 'success',
        'data': [dpt.to_dict() for dpt in dpts]
    })

@app.route('/api/dpts/<string:dpt_id>', methods=['GET'])
def get_dpt(dpt_id):
    """Obtener un DPT específico"""
    dpt = DPT.query.get_or_404(dpt_id)
    return jsonify({
        'status': 'success',
        'data': dpt.to_dict()
    })

@app.route('/api/dpts', methods=['POST'])
def create_dpt():
    """Crear un nuevo DPT"""
    data = request.json
    
    # Validar datos requeridos
    required_fields = ['title', 'department', 'format_id', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': 'Faltan campos requeridos'
        }), 400
        
    # Evaluar calidad
    quality_score = evaluate_quality(data['content'], data['format_id'])
    
    # Crear nuevo DPT
    new_dpt = DPT(
        title=data['title'],
        department=data['department'],
        format_id=data['format_id'],
        content=data['content'],
        created_by=data.get('created_by', 'system'),
        status=data.get('status', 'active'),
        quality_score=quality_score
    )
    
    db.session.add(new_dpt)
    db.session.commit()
    
    # Crear versión inicial
    initial_version = DPTVersion(
        dpt_id=new_dpt.id,
        content=data['content'],
        created_by=data.get('created_by', 'system'),
        version_number=1,
        change_notes='Versión inicial'
    )
    
    db.session.add(initial_version)
    db.session.commit()
    
    # Guardar en GitHub si está configurado
    github_result = None
    if GITHUB_TOKEN and GITHUB_TOKEN != 'tu_token_github_aqui':
        success, message = save_to_github(new_dpt)
        github_result = {'success': success, 'message': message}
    
    return jsonify({
        'status': 'success',
        'message': 'DPT creado correctamente',
        'data': new_dpt.to_dict(),
        'quality_score': quality_score,
        'github_result': github_result
    }), 201

@app.route('/api/dpts/<string:dpt_id>', methods=['PUT'])
def update_dpt(dpt_id):
    """Actualizar un DPT existente"""
    dpt = DPT.query.get_or_404(dpt_id)
    data = request.json
    
    # Guardar versión anterior
    current_version_num = DPTVersion.query.filter_by(dpt_id=dpt_id).count() + 1
    
    previous_version = DPTVersion(
        dpt_id=dpt.id,
        content=dpt.content,
        created_by=data.get('updated_by', 'system'),
        version_number=current_version_num,
        change_notes=data.get('change_notes', 'Actualización')
    )
    
    db.session.add(previous_version)
    
    # Actualizar DPT
    if 'title' in data:
        dpt.title = data['title']
    if 'department' in data:
        dpt.department = data['department']
    if 'format_id' in data:
        dpt.format_id = data['format_id']
    if 'content' in data:
        dpt.content = data['content']
        # Re-evaluar calidad
        dpt.quality_score = evaluate_quality(data['content'], dpt.format_id)
    if 'status' in data:
        dpt.status = data['status']
        
    db.session.commit()
    
    # Actualizar en GitHub si está configurado
    github_result = None
    if GITHUB_TOKEN and GITHUB_TOKEN != 'tu_token_github_aqui':
        success, message = save_to_github(dpt)
        github_result = {'success': success, 'message': message}
    
    return jsonify({
        'status': 'success',
        'message': 'DPT actualizado correctamente',
        'data': dpt.to_dict(),
        'github_result': github_result
    })

@app.route('/api/dpts/<string:dpt_id>/versions', methods=['GET'])
def get_dpt_versions(dpt_id):
    """Obtener historial de versiones de un DPT"""
    DPT.query.get_or_404(dpt_id)  # Verificar que el DPT existe
    
    versions = DPTVersion.query.filter_by(dpt_id=dpt_id).order_by(DPTVersion.version_number.desc()).all()
    
    return jsonify({
        'status': 'success',
        'data': [{
            'version_number': v.version_number,
            'created_at': v.created_at.isoformat(),
            'created_by': v.created_by,
            'change_notes': v.change_notes,
            'content': v.content
        } for v in versions]
    })

@app.route('/api/analyze/file', methods=['POST'])
def analyze_file():
    """Analizar un archivo DPT"""
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No se ha proporcionado ningún archivo'
        }), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No se ha seleccionado ningún archivo'
        }), 400
        
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': f'Tipo de archivo no permitido. Formatos soportados: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
        
    # Guardar archivo temporalmente
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Extraer texto según el tipo de archivo
    try:
        if filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.txt') or filename.endswith('.md') or filename.endswith('.rtf'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            # Nunca debería llegar aquí por la validación anterior
            return jsonify({
                'status': 'error',
                'message': 'Formato de archivo no soportado'
            }), 400
        
        # Analizar el documento
        options = request.form
        results = {}
        
        # Detectar formato si se solicita
        if 'identify_format' in options and options['identify_format'] == 'true':
            format_id, confidence = detect_format(text)
            format_obj = FormatTemplate.query.get(format_id)
            results['format'] = {
                'id': format_id,
                'name': format_obj.name if format_obj else "Desconocido",
                'confidence': confidence
            }
        
        # Extraer componentes si se solicita
        if 'extract_components' in options and options['extract_components'] == 'true':
            format_id = results.get('format', {}).get('id', 1)  # Usar formato detectado o el predeterminado
            components = extract_components(text, format_id)
            results['components'] = components
        
        # Evaluar calidad si se solicita
        if 'quality_check' in options and options['quality_check'] == 'true' and 'components' in results:
            format_id = results.get('format', {}).get('id', 1)
            quality_score = evaluate_quality(results['components'], format_id)
            results['quality'] = {
                'overall_score': quality_score,
                'details': {
                    'completeness': quality_score * 0.4 * 2.5,  # Aproximación
                    'clarity': quality_score * 0.2 * 5.0,       # Aproximación
                    'specificity': quality_score * 0.2 * 5.0,   # Aproximación
                    'measurability': quality_score * 0.2 * 5.0  # Aproximación
                }
            }
        
        # Sugerir mejoras si se solicita
        if 'suggest_improvements' in options and options['suggest_improvements'] == 'true' and 'components' in results:
            format_id = results.get('format', {}).get('id', 1)
            quality_details = results.get('quality', {}).get('details')
            suggestions = suggest_improvements(results['components'], format_id, quality_details)
            results['suggestions'] = suggestions
            
        # Limpiar el archivo temporal
        os.remove(file_path)
        
        return jsonify({
            'status': 'success',
            'data': results
        })
        
    except Exception as e:
        # En caso de error, asegurarse de limpiar el archivo
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify({
            'status': 'error',
            'message': f'Error al procesar el archivo: {str(e)}'
        }), 500

@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    """Analizar texto de DPT"""
    data = request.json
    
    if 'text' not in data or not data['text'].strip():
        return jsonify({
            'status': 'error',
            'message': 'No se ha proporcionado texto para analizar'
        }), 400
        
    text = data['text']
    options = data.get('options', {})
    results = {}
    
    # Detectar formato si se solicita
    if options.get('identify_format', False):
        format_id, confidence = detect_format(text)
        format_obj = FormatTemplate.query.get(format_id)
        results['format'] = {
            'id': format_id,
            'name': format_obj.name if format_obj else "Desconocido",
            'confidence': confidence
        }
    
    # Extraer componentes si se solicita
    if options.get('extract_components', False):
        format_id = results.get('format', {}).get('id', 1)  # Usar formato detectado o el predeterminado
        components = extract_components(text, format_id)
        results['components'] = components
    
    # Evaluar calidad si se solicita
    if options.get('quality_check', False) and 'components' in results:
        format_id = results.get('format', {}).get('id', 1)
        quality_score = evaluate_quality(results['components'], format_id)
        results['quality'] = {
            'overall_score': quality_score,
            'details': {
                'completeness': quality_score * 0.4 * 2.5,  # Aproximación
                'clarity': quality_score * 0.2 * 5.0,       # Aproximación
                'specificity': quality_score * 0.2 * 5.0,   # Aproximación
                'measurability': quality_score * 0.2 * 5.0  # Aproximación
            }
        }
    
    # Sugerir mejoras si se solicita
    if options.get('suggest_improvements', False) and 'components' in results:
        format_id = results.get('format', {}).get('id', 1)
        quality_details = results.get('quality', {}).get('details')
        suggestions = suggest_improvements(results['components'], format_id, quality_details)
        results['suggestions'] = suggestions
        
    return jsonify({
        'status': 'success',
        'data': results
    })

@app.route('/api/convert', methods=['POST'])
def convert_dpt_format():
    """Convertir un DPT de un formato a otro"""
    data = request.json
    
    if not all(k in data for k in ['content', 'source_format_id', 'target_format_id']):
        return jsonify({
            'status': 'error',
            'message': 'Faltan campos requeridos'
        }), 400
        
    converted = convert_to_format(
        data['content'],
        data['source_format_id'],
        data['target_format_id']
    )
    
    return jsonify({
        'status': 'success',
        'data': {
            'converted_content': converted,
            'source_format_id': data['source_format_id'],
            'target_format_id': data['target_format_id']
        }
    })

@app.route('/api/ai/assist', methods=['POST'])
def ai_assist():
    """Obtener asistencia de IA para redacción"""
    data = request.json
    
    if 'query' not in data:
        return jsonify({
            'status': 'error',
            'message': 'No se ha proporcionado consulta'
        }), 400
        
    query = data['query']
    context = data.get('context', {})
    field = data.get('field', '')
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Preparar prompt según el contexto
        if field and context:
            prompt = f"""
            Estoy redactando una Descripción de Puesto de Trabajo y necesito ayuda con el campo "{field}".
            
            Aquí está la información que ya tengo del puesto:
            Título: {context.get('title', '')}
            Departamento: {context.get('department', '')}
            
            Mi consulta es: {query}
            
            Por favor, proporciona una redacción profesional, clara y específica para este campo.
            """
        else:
            prompt = f"""
            Estoy redactando una Descripción de Puesto de Trabajo y necesito ayuda.
            
            Mi consulta es: {query}
            
            Por favor, proporciona una respuesta profesional y útil para ayudarme con esta descripción de puesto.
            """
            
        response = model.generate_content(prompt)
        
        return jsonify({
            'status': 'success',
            'data': {
                'response': response.text
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al procesar la consulta con IA: {str(e)}'
        }), 500

@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    """Generar informe de DPTs"""
    data = request.json
    dpt_ids = data.get('dpt_ids')  # Opcional, si es None se generará para todos
    
    success, report_path = generate_dpt_report(dpt_ids)
    
    if success:
        # Opciones para descargar el informe
        return jsonify({
            'status': 'success',
            'data': {
                'report_path': report_path,
                'download_url': f'/api/reports/download?path={report_path}'
            }
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Error al generar informe: {report_path}'
        }), 500

@app.route('/api/reports/download', methods=['GET'])
def download_report():
    """Descargar un informe generado"""
    report_path = request.args.get('path')
    
    if not report_path or not os.path.exists(report_path):
        return jsonify({
            'status': 'error',
            'message': 'Informe no encontrado'
        }), 404
        
    return send_file(report_path, as_attachment=True)

# Ruta principal para servir la aplicación frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_file(os.path.join(app.static_folder, path))
    else:
        return send_file(os.path.join(app.static_folder, 'index.html'))

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
import os
import json
import uuid
import datetime
import re
import shutil
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy.dialects.postgresql import JSON
import google.generativeai as genai
import requests
from github import Github
import docx
import fitz  # PyMuPDF
import markdown2
import pandas as pd

# Configuración de la aplicación
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dpt_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuración de carga de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'txt', 'rtf', 'md'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuración de Gemini AI (reemplazar con tus credenciales)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'tu_api_key_aqui')
genai.configure(api_key=GEMINI_API_KEY)

# Configuración de GitHub (reemplazar con tus credenciales)
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', 'tu_token_github_aqui')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'nombre_usuario/nombre_repo')
github_client = Github(GITHUB_TOKEN)

# Definición de modelos de datos
class DPT(db.Model):
    """Modelo para almacenar las Descripciones de Puesto de Trabajo"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    format_id = db.Column(db.Integer, nullable=False)
    content = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, draft, archived
    quality_score = db.Column(db.Float)  # Puntuación de calidad calculada
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'department': self.department,
            'format_id': self.format_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by,
            'status': self.status,
            'quality_score': self.quality_score
        }

class DPTVersion(db.Model):
    """Modelo para almacenar versiones históricas de DPTs"""
    id = db.Column(db.Integer, primary_key=True)
    dpt_id = db.Column(db.String(36), db.ForeignKey('dpt.id'), nullable=False)
    content = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.String(100))
    version_number = db.Column(db.Integer, nullable=False)
    change_notes = db.Column(db.Text)
    
    dpt = db.relationship('DPT', backref=db.backref('versions', lazy=True))

class FormatTemplate(db.Model):
    """Modelo para almacenar plantillas de formatos de DPT"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    structure = db.Column(JSON, nullable=False)  # Estructura de campos
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

# Inicialización de la base de datos
with app.app_context():
    db.create_all()
    
    # Crear formatos de plantilla si no existen
    if FormatTemplate.query.count() == 0:
        formats = [
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
            # Continuar con el resto de formatos...
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
            # Resto de formatos...
        ]
        
        for format_data in formats:
            format_template = FormatTemplate(
                name=format_data['name'],
                description=format_data['description'],
                structure=format_data['structure']
            )
            db.session.add(format_template)
        
        db.session.commit()

# Funciones de utilidad
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def detect_format(text):
    """
    Detecta el formato de DPT basado en el contenido
    Retorna el ID del formato y el nivel de confianza
    """
    # Obtener todos los formatos
    formats = FormatTemplate.query.all()
    
    # Inicializar puntuaciones
    format_scores = []
    
    for fmt in formats:
        score = 0
        total_fields = len(fmt.structure)
        matched_fields = 0
        
        # Buscar cada campo en el texto
        for field_name, field_info in fmt.structure.items():
            # Crear patrones de búsqueda basados en las etiquetas de los campos
            search_patterns = [
                field_info['label'],
                field_name.replace('_', ' ').title()
            ]
            
            # Verificar si alguno de los patrones está en el texto
            if any(re.search(fr'\b{pattern}\b', text, re.IGNORECASE) for pattern in search_patterns):
                matched_fields += 1
        
        # Calcular puntuación como porcentaje de campos encontrados
        score = (matched_fields / total_fields) * 100
        format_scores.append({'id': fmt.id, 'name': fmt.name, 'score': score})
    
    # Ordenar por puntuación descendente
    format_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Retornar el formato con mayor puntuación
    if format_scores and format_scores[0]['score'] > 30:  # Mínimo 30% de coincidencia
        return format_scores[0]['id'], format_scores[0]['score']
    else:
        return 1, 0  # Formato por defecto si no se detecta ninguno

def extract_components(text, format_id):
    """
    Extrae los componentes del DPT basado en el formato
    """
    format_template = FormatTemplate.query.get(format_id)
    if not format_template:
        return {}
    
    components = {}
    
    # Utilizar IA para extraer componentes
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Preparar prompt para la IA
    fields_list = ', '.join([f"'{field}': {info['label']}" for field, info in format_template.structure.items()])
    
    prompt = f"""
    A continuación te presento el texto de una Descripción de Puesto de Trabajo.
    
    Necesito que extraigas la información para los siguientes campos:
    {fields_list}
    
    Devuelve la información en formato JSON.
    Si no encuentras información para algún campo, déjalo vacío.
    
    Texto del DPT:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        # Intentar extraer el JSON de la respuesta
        match = re.search(r'```json\s*(.*?)\s*```', response.text, re.DOTALL)
        if match:
            json_str = match.group(1)
            components = json.loads(json_str)
        else:
            # Intentar cargar directamente como JSON
            components = json.loads(response.text)
    except Exception as e:
        print(f"Error al extraer componentes con IA: {e}")
        # Fallback manual: buscar patrones simples en el texto
        for field, info in format_template.structure.items():
            pattern = fr'{info["label"]}[\s:]*(.*?)(?:\n\n|\n[A-Z]|$)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                components[field] = match.group(1).strip()
            else:
                components[field] = ""
    
    return components

def evaluate_quality(dpt_content, format_id):
    """
    Evalúa la calidad del DPT
    """
    format_template = FormatTemplate.query.get(format_id)
    if not format_template:
        return 0
    
    # Criterios de evaluación
    criteria = {
        'completeness': 0,  # Completitud de campos requeridos
        'clarity': 0,       # Claridad de redacción
        'specificity': 0,   # Especificidad de responsabilidades y requisitos
        'measurability': 0  # Uso de criterios medibles/cuantificables
    }
    
    # 1. Evaluar completitud
    required_fields = [f for f, info in format_template.structure.items() if info.get('required', False)]
    filled_required = sum(1 for f in required_fields if f in dpt_content and dpt_content[f].strip())
    criteria['completeness'] = (filled_required / len(required_fields)) * 100 if required_fields else 0
    
    # 2. Usar IA para evaluar claridad, especificidad y medibilidad
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convertir el contenido a texto para evaluación
        content_text = "\n\n".join([f"{format_template.structure[k]['label']}:\n{v}" for k, v in dpt_content.items() if v])
        
        prompt = f"""
        Evalúa la siguiente Descripción de Puesto de Trabajo y asigna una puntuación de 0 a 100 para cada uno de estos criterios:
        
        1. Claridad: ¿Es fácil de entender? ¿Utiliza lenguaje claro y directo?
        2. Especificidad: ¿Describe con detalle las responsabilidades y requisitos?
        3. Medibilidad: ¿Incluye criterios o resultados medibles/cuantificables?
        
        Responde solo con un JSON en este formato:
        {{
            "clarity": [puntuación],
            "specificity": [puntuación],
            "measurability": [puntuación]
        }}
        
        Descripción de Puesto:
        {content_text}
        """
        
        response = model.generate_content(prompt)
        
        # Extraer JSON de la respuesta
        match = re.search(r'```json\s*(.*?)\s*```', response.text, re.DOTALL)
        json_str = match.group(1) if match else response.text
        
        ai_scores = json.loads(json_str)
        criteria.update(ai_scores)
    except Exception as e:
        print(f"Error al evaluar calidad con IA: {e}")
        # Valores por defecto si falla la IA
        criteria['clarity'] = 70
        criteria['specificity'] = 70
        criteria['measurability'] = 60
    
    # Calcular puntuación general (ponderada)
    weights = {
        'completeness': 0.4,
        'clarity': 0.2,
        'specificity': 0.2,
        'measurability': 0.2
    }
    
    overall_score = sum(criteria[c] * weights[c] for c in criteria)
    return overall_score

def suggest_improvements(dpt_content, format_id, quality_scores=None):
    """
    Sugiere mejoras para el DPT
    """
    format_template = FormatTemplate.query.get(format_id)
    if not format_template:
        return []
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convertir el contenido a texto
        content_text = "\n\n".join([f"{format_template.structure[k]['label']}:\n{v}" for k, v in dpt_content.items() if v])
        
        # Incluir información de calidad si está disponible
        quality_info = ""
        if quality_scores:
            quality_info = "Puntuaciones de calidad:\n"
            for criterion, score in quality_scores.items():
                quality_info += f"- {criterion}: {score}/100\n"
        
        prompt = f"""
        Analiza la siguiente Descripción de Puesto de Trabajo y sugiere mejoras concretas.
        
        {quality_info}
        
        Enfócate en:
        1. Campos incompletos o con poca información
        2. Claridad de la redacción
        3. Especificidad de responsabilidades y requisitos
        4. Inclusión de métricas o indicadores medibles
        5. Coherencia general del documento
        
        