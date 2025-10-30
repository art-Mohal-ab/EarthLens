import React, { useState, useEffect } from 'react';
import api, { API_BASE_URL } from '../services/api';

const ViewReportModal = ({ report, isOpen, onClose }) => {
  const [comments, setComments] = useState([]);
  const [isReplying, setIsReplying] = useState(false);
  const [replyText, setReplyText] = useState('');
  const [loadingComments, setLoadingComments] = useState(false);
  const [submittingComment, setSubmittingComment] = useState(false);
  const [aiRecommendations, setAiRecommendations] = useState([]);

  useEffect(() => {
    if (isOpen && report) {
      fetchComments();
      parseAiRecommendations();
    }
  }, [isOpen, report]);

  const fetchComments = async () => {
    try {
      setLoadingComments(true);
      const response = await api.get(`/comments/report/${report.id}`);
      setComments(response.data.comments || []);
    } catch (error) {
      console.error('Error fetching comments:', error);
      setComments([]);
    } finally {
      setLoadingComments(false);
    }
  };

  const parseAiRecommendations = () => {
    if (report.ai_advice) {
      const lines = report.ai_advice.split('\n').filter(line => line.trim());
      const recommendations = lines
        .filter(line => line.match(/^[-•*]|^\d+\./))
        .map(line => line.replace(/^[-•*]|^\d+\./, '').trim())
        .filter(line => line.length > 0);
      
      if (recommendations.length > 0) {
        setAiRecommendations(recommendations);
      } else {
        setAiRecommendations([report.ai_advice]);
      }
    } else {
      setAiRecommendations(['AI analysis is being processed. Check back later for recommendations.']);
    }
  };

  if (!isOpen || !report) return null;

  const handleReplyClick = () => {
    setIsReplying(!isReplying);
  };

  const handleReplySubmit = async () => {
    if (replyText.trim()) {
      try {
        setSubmittingComment(true);
        const response = await api.post('/comments', {
          content: replyText,
          report_id: report.id
        });
        
        await fetchComments();
        setReplyText('');
        setIsReplying(false);
      } catch (error) {
        console.error('Error submitting comment:', error);
        alert('Failed to post comment. Please try again.');
      } finally {
        setSubmittingComment(false);
      }
    }
  };

  return (
    <div className="view-modal-overlay" onClick={onClose}>
      <div className="view-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="view-close-btn" onClick={onClose}>×</button>

        <div className="view-modal-image">
          <img
            src={report.image_url ? `${API_BASE_URL.replace('/api', '')}${report.image_url}` : '/placeholder.png'}
            alt={report.title}
            onError={(e) => { e.target.src = '/placeholder.png'; }}
          />
        </div>

        <div className="view-modal-body">
          <div className="view-report-description">
            <h3>Report Description</h3>
            <p>{report.description}</p>
            <div className="report-meta">
              <span>Location: {report.location}</span>
              <span>Category: {report.ai_category}</span>
              <span>Reported by: {report.user?.username || 'Anonymous'}</span>
              <span>Date: {new Date(report.created_at).toLocaleDateString()}</span>
            </div>
          </div>

          <div className="view-ai-recommendations">
            <h3>AI Recommendations</h3>
            <ul>
              {aiRecommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>

          <div className="view-comments-section">
            <h3>Comments</h3>
            {loadingComments ? (
              <p>Loading comments...</p>
            ) : comments.length === 0 ? (
              <p>No comments yet. Be the first to comment!</p>
            ) : (
              comments.map(comment => (
                <div key={comment.id} className="comment">
                  <div className="comment-avatar">
                    {comment.author?.username?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div className="comment-content">
                    <div className="comment-user">{comment.author?.username || 'Anonymous'}</div>
                    <div className="comment-text">{comment.content}</div>
                    <small>{new Date(comment.created_at).toLocaleString()}</small>
                    {comment.is_edited && <small className="edited-badge"> (edited)</small>}
                  </div>
                </div>
              ))
            )}
            {!isReplying ? (
              <button onClick={handleReplyClick} className="add-comment-btn">Add Comment</button>
            ) : (
              <div className="reply-section">
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  placeholder="Write your comment..."
                  rows="3"
                  disabled={submittingComment}
                />
                <button 
                  onClick={handleReplySubmit} 
                  className="submit-reply-btn"
                  disabled={submittingComment || !replyText.trim()}
                >
                  {submittingComment ? 'Posting...' : 'Post Comment'}
                </button>
                <button 
                  onClick={() => {
                    setIsReplying(false);
                    setReplyText('');
                  }} 
                  className="cancel-reply-btn"
                  disabled={submittingComment}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewReportModal;
