from flask import Blueprint, request, jsonify, send_file
import os
import zipfile
import traceback
from pathlib import Path

from converters.pdf_converter import PDFConverter
from converters.image_converter import ImageConverter
from converters.document_converter import DocumentConverter
from utils.file_handler import save_upload, remove_file, create_output_dir, get_file_extension

conversion_bp = Blueprint('conversion', __name__, url_prefix='/api')

# Formatos de saída disponíveis por extensão do arquivo de entrada
SUPPORTED_CONVERSIONS = {
    'pdf':  ['PNG', 'JPG', 'TXT', 'DOCX', 'XLSX', 'COMPRESS'],
    'png':  ['PDF', 'JPG', 'WEBP'],
    'jpg':  ['PDF', 'PNG', 'WEBP'],
    'jpeg': ['PDF', 'PNG', 'WEBP'],
    'webp': ['PDF', 'PNG', 'JPG'],
    'gif':  ['PDF', 'PNG', 'JPG'],
    'bmp':  ['PDF', 'PNG', 'JPG'],
    'docx': ['PDF', 'TXT'],
    'xlsx': ['PDF', 'CSV', 'TXT'],
    'pptx': ['PDF', 'TXT'],
    'txt':  ['PDF', 'DOCX'],
    'csv':  ['XLSX', 'TXT'],
}


def _run_conversion(filepath, file_ext, format_upper):
    """Roteia a conversão para o conversor correto e retorna (files, error)."""

    # ── PDF ──────────────────────────────────────────────────────────────
    if file_ext == 'pdf':
        converter = PDFConverter(filepath)
        if format_upper in ('PNG', 'JPG'):
            return converter.to_images(format=format_upper)
        if format_upper == 'TXT':
            return converter.to_text()
        if format_upper == 'DOCX':
            return converter.to_docx()
        if format_upper == 'XLSX':
            return converter.to_xlsx()
        if format_upper == 'COMPRESS':
            return converter.compress_pdf()

    # ── Imagens ──────────────────────────────────────────────────────────
    if file_ext in ('png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'):
        converter = ImageConverter(filepath)
        if format_upper == 'PDF':
            return converter.to_pdf()
        return converter.to_image(format=format_upper)

    # ── Documentos / Planilhas / Texto ───────────────────────────────────
    converter = DocumentConverter(filepath)

    if file_ext == 'docx':
        if format_upper == 'PDF':
            return converter.docx_to_pdf()
        if format_upper == 'TXT':
            return converter.docx_to_txt()

    if file_ext == 'xlsx':
        if format_upper == 'PDF':
            return converter.xlsx_to_pdf()
        if format_upper == 'CSV':
            return converter.xlsx_to_csv()
        if format_upper == 'TXT':
            return converter.xlsx_to_txt()

    if file_ext == 'pptx':
        if format_upper == 'PDF':
            return converter.pptx_to_pdf()
        if format_upper == 'TXT':
            return converter.pptx_to_txt()

    if file_ext == 'txt':
        if format_upper == 'PDF':
            return converter.txt_to_pdf()
        if format_upper == 'DOCX':
            return converter.txt_to_docx()

    if file_ext == 'csv':
        if format_upper == 'XLSX':
            return converter.csv_to_xlsx()
        if format_upper == 'TXT':
            return converter.csv_to_txt()

    return None, f"Conversão {file_ext.upper()} → {format_upper} não suportada"


@conversion_bp.route('/convert', methods=['POST'])
def convert_file():
    """Endpoint universal de conversão de arquivos."""

    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    if 'formats' not in request.form:
        return jsonify({'error': 'Nenhum formato selecionado'}), 400

    file = request.files['file']
    formats = request.form.getlist('formats')

    if not formats:
        return jsonify({'error': 'Nenhum formato selecionado'}), 400

    # Salvar arquivo (validação interna)
    filepath, msg = save_upload(file)
    if not filepath:
        return jsonify({'error': msg}), 400

    file_ext = get_file_extension(filepath)
    allowed = SUPPORTED_CONVERSIONS.get(file_ext, [])

    # Validar formatos solicitados contra o tipo do arquivo
    invalid = [f for f in formats if f.upper() not in allowed]
    if invalid:
        remove_file(filepath)
        return jsonify({'error': f'Formatos inválidos para .{file_ext}: {invalid}'}), 400

    output_dir = create_output_dir()

    try:
        output_files = []
        errors = []

        for fmt in formats:
            files, error = _run_conversion(filepath, file_ext, fmt.upper())
            if error:
                errors.append(f"{fmt.upper()}: {error}")
            elif files:
                output_files.extend(files)

        remove_file(filepath)

        if not output_files:
            return jsonify({'error': 'Falha na conversão: ' + ' | '.join(errors)}), 500

        # Arquivo único → retornar direto
        if len(output_files) == 1:
            fp = output_files[0]
            return send_file(fp, as_attachment=True, download_name=os.path.basename(fp))

        # Múltiplos arquivos → ZIP
        zip_filename = f"{Path(filepath).stem}_converted.zip"
        zip_path = os.path.join(output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for fp in output_files:
                zipf.write(fp, arcname=os.path.basename(fp))
        for fp in output_files:
            remove_file(fp)

        return send_file(zip_path, as_attachment=True, download_name=zip_filename)

    except Exception as e:
        print(f"ERRO GERAL NA CONVERSÃO: {str(e)}")
        print(traceback.format_exc())
        remove_file(filepath)
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500


@conversion_bp.route('/formats', methods=['GET'])
def get_formats():
    """Retorna formatos de saída disponíveis por tipo de arquivo."""
    return jsonify(SUPPORTED_CONVERSIONS), 200


@conversion_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar saúde da API."""
    return jsonify({'status': 'ok'}), 200


# ───────────────── OPERAÇÕES DE PDF ─────────────────

@conversion_bp.route('/merge', methods=['POST'])
def merge_pdfs():
    """Une múltiplos PDFs em um único arquivo."""
    if 'files' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    files = request.files.getlist('files')
    if len(files) < 2:
        return jsonify({'error': 'Envie pelo menos 2 arquivos PDF para unir'}), 400

    filepaths = []
    try:
        for file in files:
            if file.filename == '':
                continue
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': 'Todos os arquivos devem ser PDF'}), 400
            filepath, msg = save_upload(file)
            if not filepath:
                return jsonify({'error': msg}), 400
            filepaths.append(filepath)

        if len(filepaths) < 2:
            return jsonify({'error': 'Envie pelo menos 2 arquivos PDF válidos'}), 400

        # Usar o primeiro como base
        converter = PDFConverter(filepaths[0])
        output_files, error = converter.merge_pdfs(filepaths[1:])

        # Limpar arquivos temporários
        for fp in filepaths:
            remove_file(fp)

        if error:
            return jsonify({'error': error}), 500

        return send_file(output_files[0], as_attachment=True, download_name=os.path.basename(output_files[0]))

    except Exception as e:
        for fp in filepaths:
            remove_file(fp)
        print(f"ERRO MERGE: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500


@conversion_bp.route('/split', methods=['POST'])
def split_pdf():
    """Divide PDF em múltiplos arquivos."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    split_mode = request.form.get('split_mode', 'all')
    page_ranges = request.form.get('page_ranges')

    filepath, msg = save_upload(file)
    if not filepath:
        return jsonify({'error': msg}), 400

    if not filepath.lower().endswith('.pdf'):
        remove_file(filepath)
        return jsonify({'error': 'Arquivo deve ser PDF'}), 400

    try:
        converter = PDFConverter(filepath)

        # Parse page_ranges se fornecido
        parsed_ranges = None
        if page_ranges:
            try:
                if split_mode == 'range':
                    # Formato: "1-3,5-7"
                    parsed_ranges = []
                    for part in page_ranges.split(','):
                        start, end = map(int, part.split('-'))
                        parsed_ranges.append((start, end))
                elif split_mode == 'every_n':
                    parsed_ranges = int(page_ranges)
            except Exception:
                remove_file(filepath)
                return jsonify({'error': 'Formato de page_ranges inválido. Use "1-3,5-7" para ranges ou número para every_n'}), 400

        output_files, error = converter.split_pdf(split_mode, parsed_ranges)
        remove_file(filepath)

        if error:
            return jsonify({'error': error}), 500

        if not output_files:
            return jsonify({'error': 'Nenhum arquivo gerado'}), 500

        # Se apenas 1 arquivo, retorna direto
        if len(output_files) == 1:
            return send_file(output_files[0], as_attachment=True, download_name=os.path.basename(output_files[0]))

        # Múltiplos → ZIP
        output_dir = create_output_dir()
        zip_filename = f"{Path(filepath).stem}_split.zip"
        zip_path = os.path.join(output_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for fp in output_files:
                zipf.write(fp, arcname=os.path.basename(fp))
        for fp in output_files:
            remove_file(fp)

        return send_file(zip_path, as_attachment=True, download_name=zip_filename)

    except Exception as e:
        remove_file(filepath)
        print(f"ERRO SPLIT: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500


@conversion_bp.route('/rotate', methods=['POST'])
def rotate_pdf():
    """Rotaciona páginas do PDF."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    rotation = request.form.get('rotation', '90')
    page_numbers = request.form.get('page_numbers')

    filepath, msg = save_upload(file)
    if not filepath:
        return jsonify({'error': msg}), 400

    if not filepath.lower().endswith('.pdf'):
        remove_file(filepath)
        return jsonify({'error': 'Arquivo deve ser PDF'}), 400

    try:
        rotation = int(rotation)
        if rotation not in (90, 180, 270):
            remove_file(filepath)
            return jsonify({'error': 'Rotação deve ser 90, 180 ou 270 graus'}), 400

        parsed_pages = None
        if page_numbers:
            try:
                parsed_pages = [int(p.strip()) for p in page_numbers.split(',') if p.strip()]
            except Exception:
                remove_file(filepath)
                return jsonify({'error': 'Números de página inválidos. Use vírgula: "1,3,5"'}), 400

        converter = PDFConverter(filepath)
        output_files, error = converter.rotate_pages(rotation, parsed_pages)
        remove_file(filepath)

        if error:
            return jsonify({'error': error}), 500

        return send_file(output_files[0], as_attachment=True, download_name=os.path.basename(output_files[0]))

    except Exception as e:
        remove_file(filepath)
        print(f"ERRO ROTATE: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500


@conversion_bp.route('/watermark', methods=['POST'])
def watermark_pdf():
    """Adiciona marca d'água ao PDF."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    watermark_text = request.form.get('watermark_text', '')
    opacity = float(request.form.get('opacity', 0.3))
    angle = int(request.form.get('angle', 45))
    font_size = int(request.form.get('font_size', 48))
    color = request.form.get('color', 'gray')

    if not watermark_text:
        return jsonify({'error': 'Texto da marca d\'água é obrigatório'}), 400

    filepath, msg = save_upload(file)
    if not filepath:
        return jsonify({'error': msg}), 400

    if not filepath.lower().endswith('.pdf'):
        remove_file(filepath)
        return jsonify({'error': 'Arquivo deve ser PDF'}), 400

    try:
        converter = PDFConverter(filepath)
        output_files, error = converter.add_watermark(
            watermark_text, opacity, angle, font_size, color
        )
        remove_file(filepath)

        if error:
            return jsonify({'error': error}), 500

        return send_file(output_files[0], as_attachment=True, download_name=os.path.basename(output_files[0]))

    except Exception as e:
        remove_file(filepath)
        print(f"ERRO WATERMARK: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500


@conversion_bp.route('/protect', methods=['POST'])
def protect_pdf():
    """Protege PDF com senha."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    user_password = request.form.get('user_password', '')
    owner_password = request.form.get('owner_password')
    permissions = request.form.get('permissions')

    if not user_password:
        return jsonify({'error': 'Senha é obrigatória'}), 400

    filepath, msg = save_upload(file)
    if not filepath:
        return jsonify({'error': msg}), 400

    if not filepath.lower().endswith('.pdf'):
        remove_file(filepath)
        return jsonify({'error': 'Arquivo deve ser PDF'}), 400

    try:
        parsed_permissions = None
        if permissions:
            try:
                import json
                parsed_permissions = json.loads(permissions)
            except Exception:
                pass

        converter = PDFConverter(filepath)
        output_files, error = converter.add_password(
            user_password, owner_password, parsed_permissions
        )
        remove_file(filepath)

        if error:
            return jsonify({'error': error}), 500

        return send_file(output_files[0], as_attachment=True, download_name=os.path.basename(output_files[0]))

    except Exception as e:
        remove_file(filepath)
        print(f"ERRO PROTECT: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500
