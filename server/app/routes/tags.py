from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.database import db
from app.models.tag import Tag
from app.schemas.tag import TagCreateSchema, TagUpdateSchema
from app.middleware.auth import auth_required

tags_bp = Blueprint('tags', __name__)

# Initialize schemas
tag_create_schema = TagCreateSchema()
tag_update_schema = TagUpdateSchema()


@tags_bp.route('', methods=['GET'])
def get_tags():
    """Get all tags with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        search = request.args.get('search', '').strip()
        
        query = Tag.query.filter(Tag.is_active == True)
        
        if search:
            query = query.filter(Tag.name.contains(search.lower()))
        
        tags = query.order_by(Tag.name)\
                   .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'tags': [tag.to_dict() for tag in tags.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': tags.total,
                'pages': tags.pages
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get tags', 'message': str(e)}), 500


@tags_bp.route('/popular', methods=['GET'])
def get_popular_tags():
    """Get most popular tags"""
    try:
        limit = min(request.args.get('limit', 20, type=int), 50)
        
        tags = Tag.get_popular_tags(limit=limit)
        
        return jsonify({
            'tags': [tag.to_dict() for tag in tags]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get popular tags', 'message': str(e)}), 500


@tags_bp.route('/search', methods=['GET'])
def search_tags():
    """Search tags by name"""
    try:
        query = request.args.get('q', '').strip()
        limit = min(request.args.get('limit', 10, type=int), 50)
        
        if not query:
            return jsonify({'tags': []}), 200
        
        tags = Tag.search_tags(query, limit=limit)
        
        return jsonify({
            'tags': [tag.to_dict() for tag in tags],
            'query': query
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to search tags', 'message': str(e)}), 500


@tags_bp.route('', methods=['POST'])
@auth_required
def create_tag(current_user):
    """Create a new tag"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = tag_create_schema.load(json_data)
        
        # Check if tag already exists
        existing_tag = Tag.query.filter_by(name=data['name'].lower()).first()
        if existing_tag:
            return jsonify({
                'message': 'Tag already exists',
                'tag': existing_tag.to_dict()
            }), 200

        # Create new tag
        tag = Tag(
            name=data['name'],
            description=data.get('description'),
            color=data.get('color', '#007bff')
        )
        tag.save()

        return jsonify({
            'message': 'Tag created successfully',
            'tag': tag.to_dict()
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create tag', 'message': str(e)}), 500


@tags_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    """Get a specific tag"""
    try:
        tag = Tag.query.get_or_404(tag_id)
        
        return jsonify({
            'tag': tag.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get tag', 'message': str(e)}), 500


@tags_bp.route('/<int:tag_id>', methods=['PUT'])
@auth_required
def update_tag(tag_id, current_user):
    """Update a tag (admin only in production)"""
    try:
        tag = Tag.query.get_or_404(tag_id)
        
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = tag_update_schema.load(json_data)
        
        # Update tag fields
        for field in ['name', 'description', 'color']:
            if field in data:
                if field == 'name':
                    # Check for name conflicts
                    existing = Tag.query.filter_by(name=data[field].lower()).first()
                    if existing and existing.id != tag_id:
                        return jsonify({'error': 'Tag name already exists'}), 400
                    setattr(tag, field, data[field].lower())
                else:
                    setattr(tag, field, data[field])
        
        tag.save()

        return jsonify({
            'message': 'Tag updated successfully',
            'tag': tag.to_dict()
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update tag', 'message': str(e)}), 500