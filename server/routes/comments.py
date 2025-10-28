from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from middleware.auth import auth_required
from models.comment import Comment
from schemas.comment import comment_create_schema, comment_update_schema
from database import db

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

# ---------------------- CREATE COMMENT ----------------------
@comments_bp.route('', methods=['POST'])
@auth_required
def create_comment(current_user):
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        validated_data = comment_create_schema.load(json_data)
        validated_data['user_id'] = current_user.id

        comment = Comment(**validated_data)
        comment.save()

        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create comment', 'message': str(e)}), 500

# ---------------------- READ COMMENTS FOR A REPORT ----------------------
@comments_bp.route('/report/<int:report_id>', methods=['GET'])
def get_report_comments(report_id):
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        offset = max(int(request.args.get('offset', 0)), 0)

        comments = Comment.get_report_comments(report_id, limit=limit, offset=offset)
        return jsonify({
            'comments': [comment.to_dict() for comment in comments],
            'total': len(comments)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get comments', 'message': str(e)}), 500

# ---------------------- READ SINGLE COMMENT ----------------------
@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        return jsonify({'comment': comment.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve comment', 'message': str(e)}), 500

# ---------------------- UPDATE COMMENT ----------------------
@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@auth_required
def update_comment(comment_id, current_user):
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404

        if comment.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        validated_data = comment_update_schema.load(json_data)
        comment.content = validated_data['content']
        comment.save()

        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict()
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update comment', 'message': str(e)}), 500

# ---------------------- DELETE COMMENT ----------------------
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@auth_required
def delete_comment(comment_id, current_user):
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404

        if comment.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete comment', 'message': str(e)}), 500
