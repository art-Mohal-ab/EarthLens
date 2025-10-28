from flask import Blueprint, request, jsonify
from models.tag import Tag
from middleware.auth import optional_auth

tags_bp = Blueprint('tags', __name__, url_prefix='/api/tags')


# =========================================================
# 📘 GET ALL TAGS (with optional search and limit)
# =========================================================
@tags_bp.route('', methods=['GET'])
@optional_auth
def get_tags(current_user):
    """Retrieve all available tags, optionally filtered by search."""
    try:
        limit = min(int(request.args.get('limit', 50)), 100)
        search = request.args.get('search', '').strip()

        query = Tag.query
        if search:
            query = query.filter(Tag.name.ilike(f'%{search}%'))

        tags = query.order_by(Tag.name.asc()).limit(limit).all()

        return jsonify({
            'tags': [tag.to_dict(include_reports_count=True) for tag in tags],
            'count': len(tags)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve tags',
            'message': str(e)
        }), 500


# =========================================================
# 🌟 GET POPULAR TAGS
# =========================================================
@tags_bp.route('/popular', methods=['GET'])
@optional_auth
def get_popular_tags(current_user):
    """Retrieve the most used/popular tags."""
    try:
        limit = min(int(request.args.get('limit', 20)), 50)
        tags = Tag.get_popular_tags(limit=limit)

        return jsonify({
            'tags': [tag.to_dict(include_reports_count=True) for tag in tags],
            'count': len(tags)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve popular tags',
            'message': str(e)
        }), 500


# =========================================================
# 🧩 GET REPORTS ASSOCIATED WITH A TAG
# =========================================================
@tags_bp.route('/<int:tag_id>/reports', methods=['GET'])
@optional_auth
def get_tag_reports(tag_id, current_user):
    """Retrieve public reports linked to a specific tag."""
    try:
        tag = Tag.query.get(tag_id)
        if not tag:
            return jsonify({
                'error': 'Tag not found',
                'message': 'The requested tag does not exist.'
            }), 404

        limit = min(int(request.args.get('limit', 20)), 100)
        offset = max(int(request.args.get('offset', 0)), 0)

        # Safer alias for Report model
        Report = tag.reports.property.mapper.class_

        reports_query = tag.reports.filter_by(is_public=True, status='active')
        total = reports_query.count()
        reports = reports_query.order_by(Report.created_at.desc()) \
                               .offset(offset).limit(limit).all()

        return jsonify({
            'tag': tag.to_dict(),
            'reports': [report.to_dict(include_comments=False) for report in reports],
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'has_more': total > (offset + limit)
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve tag reports',
            'message': str(e)
        }), 500
