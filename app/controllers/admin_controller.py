from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

admin_controller = Blueprint('admin', __name__)

def init_admin_controller(document_service):
    """
    Initialize admin controller.
    
    Args:
        document_service: Document service
    """
    
    @admin_controller.route('/admin')
    @login_required
    def admin_panel():
        """Admin panel page."""
        # Get all documents grouped by type
        case_analysis_docs = document_service.get_documents_by_type('Case Section Analysis')
        bail_analysis_docs = document_service.get_documents_by_type('Bail Analysis')
        human_analysis_docs = document_service.get_documents_by_type('Human Analysis')
          # Get all documents for listing
        all_documents = document_service.get_all_documents()
        
        return render_template(
            'admin.html',
            case_analysis_docs=case_analysis_docs,
            bail_analysis_docs=bail_analysis_docs,
            human_analysis_docs=human_analysis_docs,
            all_documents=all_documents
        )
    
    @admin_controller.route('/admin/upload', methods=['POST'])
    @login_required
    def upload_document():
        """Handle document uploads."""
        try:
            # Check if the post request has the file part
            if 'document' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
                
            file = request.files['document']
            
            # If user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(url_for('admin.admin_panel'))
                
            title = request.form.get('title', 'Untitled Document')
            document_type = request.form.get('document_type', 'Case Section Analysis')
            
            # Validate document type
            valid_types = ['Case Section Analysis', 'Bail Analysis', 'Human Analysis']
            if document_type not in valid_types:
                flash('Invalid document type', 'danger')
                return redirect(url_for('admin.admin_panel'))
            
            # Upload document
            document = document_service.upload_document(
                file=file,
                document_type=document_type,
                title=title,
                user_id=current_user.id
            )
            
            flash(f'Document "{title}" uploaded successfully!', 'success')
            
        except Exception as e:
            flash(f'Error uploading document: {str(e)}', 'danger')
            
        return redirect(url_for('admin.admin_panel'))
    
    @admin_controller.route('/admin/documents')
    @login_required
    def manage_documents():
        """Document management page."""
        all_documents = document_service.get_all_documents()
        return render_template('manage_documents.html', documents=all_documents)
    
    @admin_controller.route('/admin/delete/<int:document_id>', methods=['POST'])
    @login_required
    def delete_document(document_id):
        """Delete document and its chunks."""
        try:
            document_service.delete_document(document_id)
            flash('Document deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting document: {str(e)}', 'error')
        return redirect(url_for('admin.manage_documents'))

    @admin_controller.route('/admin/edit/<int:document_id>')
    @login_required
    def edit_document(document_id):
        """Edit document page."""
        document = document_service.get_document_by_id(document_id)
        if not document:
            flash('Document not found!', 'error')
            return redirect(url_for('admin.manage_documents'))
        return render_template('edit_document.html', document=document)
    
    @admin_controller.route('/admin/update/<int:document_id>', methods=['POST'])
    @login_required
    def update_document(document_id):
        """Update document."""
        try:
            title = request.form.get('title')
            document_type = request.form.get('document_type')
            content = request.form.get('content')
            
            document_service.update_document(document_id, title, document_type, content)
            flash('Document updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating document: {str(e)}', 'error')
        return redirect(url_for('admin.manage_documents'))

    return admin_controller
