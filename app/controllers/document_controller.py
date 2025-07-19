from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.database import Document, Chunk

document_controller = Blueprint('document', __name__)

def init_document_controller(db_session):
    """
    Initialize document controller.
    
    Args:
        db_session: SQLAlchemy session for database operations
    """
    
    @document_controller.route('/api/document/<document_id>/source/<source_id>')
    @login_required
    def get_document_source(document_id, source_id):
        """Get document content with highlighted source text."""
        try:
            # Validate inputs
            try:
                doc_id = int(document_id)
                source_id = int(source_id)
            except ValueError:
                return jsonify({'error': 'Invalid document or source ID'}), 400
                
            # Get the document
            document = db_session.query(Document).filter(Document.document_id == doc_id).first()
            if not document:
                return jsonify({'error': 'Document not found'}), 404
                
            # Get all chunks for this document
            chunks = db_session.query(Chunk).filter(
                Chunk.document_id == doc_id
            ).order_by(Chunk.chunk_order).all()
            
            if not chunks:
                return jsonify({'error': 'No content found for this document'}), 404
                
            # Combine all chunks into full document content
            full_content = " ".join([c.chunk_text for c in chunks])
            
            # Get the target chunk to highlight
            target_chunk = db_session.query(Chunk).filter(
                Chunk.chunk_id == source_id
            ).first()
            
            # If we don't have the specific chunk ID, return the full document without highlighting
            if not target_chunk:
                return jsonify({
                    'content': full_content,
                    'highlights': [],
                    'meta': {
                        'name': document.document_name,
                        'type': document.document_type,
                        'id': document.document_id
                    }
                })
            
            # Find where in the full document this chunk appears
            chunk_text = target_chunk.chunk_text
            start_pos = full_content.find(chunk_text)
            
            # If we can find the chunk text in the full document
            if start_pos >= 0:
                end_pos = start_pos + len(chunk_text)
                highlights = [[start_pos, end_pos]]
            else:
                # Fallback: just highlight the chunk text itself
                highlights = [[0, len(chunk_text)]]
                full_content = chunk_text
            
            # Return the content with highlight information
            return jsonify({
                'content': full_content,
                'highlights': highlights,
                'meta': {
                    'name': document.document_name,
                    'type': document.document_type,
                    'id': document.document_id,
                    'source_id': target_chunk.chunk_id
                }
            })
            
        except Exception as e:
            print(f"Error getting document source: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @document_controller.route('/api/documents/types')
    @login_required
    def get_document_types():
        """Get all document types."""
        try:
            # Get unique document types
            results = db_session.query(Document.document_type).distinct().all()
            types = [r[0] for r in results if r[0]]
            
            return jsonify({'types': types})
        except Exception as e:
            print(f"Error getting document types: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    return document_controller
