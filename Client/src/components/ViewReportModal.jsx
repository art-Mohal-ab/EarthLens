import React, { useState } from 'react';
import { API_BASE_URL } from '../services/api';

const ViewReportModal = ({ report, isOpen, onClose }) => {
  const getContextualComments = (report) => {
    const baseComments = {
      "Waste Management": [
        {
          id: 1,
          user: "Waste Management Expert",
          text: "This illegal dumping is a serious violation of environmental regulations. The plastic waste can contaminate waterways for years.",
          avatar: "W",
          timestamp: "2023-10-15 10:30 AM"
        },
        {
          id: 2,
          user: "Local Community Member",
          text: "I've seen this dumping site growing for months. It's affecting the river ecosystem and fish populations.",
          avatar: "C",
          timestamp: "2023-10-15 2:45 PM"
        },
        {
          id: 3,
          user: "Environmental Activist",
          text: "We need to organize a cleanup and report this to the National Environment Management Authority immediately.",
          avatar: "A",
          timestamp: "2023-10-16 9:20 AM"
        }
      ],
      "Air Pollution": [
        {
          id: 1,
          user: "Air Quality Specialist",
          text: "These emissions likely exceed permitted levels. This could be causing respiratory issues in the surrounding community.",
          avatar: "A",
          timestamp: "2023-10-14 11:15 AM"
        },
        {
          id: 2,
          user: "Local Resident",
          text: "The smoke from this factory has been getting worse. My children have been having breathing problems.",
          avatar: "R",
          timestamp: "2023-10-14 3:30 PM"
        },
        {
          id: 3,
          user: "Environmental Engineer",
          text: "This requires immediate inspection by environmental authorities. The factory may need emission controls installed.",
          avatar: "E",
          timestamp: "2023-10-15 8:45 AM"
        }
      ],
      "Flooding": [
        {
          id: 1,
          user: "Environmental Expert",
          text: "This is a serious environmental concern that needs immediate attention. The local authorities should be notified.",
          avatar: "E",
          timestamp: "2023-10-15 10:30 AM"
        },
        {
          id: 2,
          user: "Community Member",
          text: "I've noticed this issue too. The flooding has been getting worse over the past few months.",
          avatar: "C",
          timestamp: "2023-10-15 2:45 PM"
        },
        {
          id: 3,
          user: "Local Resident",
          text: "Please help! My home was affected by the flooding last week. We need urgent action.",
          avatar: "L",
          timestamp: "2023-10-16 9:20 AM"
        }
      ],
      "Poaching": [
        {
          id: 1,
          user: "Wildlife Conservationist",
          text: "Poaching threatens endangered species and disrupts the entire ecosystem. This needs to be reported to wildlife authorities immediately.",
          avatar: "W",
          timestamp: "2023-10-10 9:00 AM"
        },
        {
          id: 2,
          user: "Local Guide",
          text: "I've seen signs of poaching in this area before. The wildlife populations are declining rapidly.",
          avatar: "G",
          timestamp: "2023-10-10 1:20 PM"
        },
        {
          id: 3,
          user: "Conservation Volunteer",
          text: "We need increased patrols and community education programs to combat poaching in this region.",
          avatar: "V",
          timestamp: "2023-10-11 10:30 AM"
        }
      ]
    };

    return baseComments[report?.ai_category] || baseComments["Flooding"];
  };

  const [comments, setComments] = useState(getContextualComments(report));
  const [isReplying, setIsReplying] = useState(false);
  const [replyText, setReplyText] = useState('');

  if (!isOpen || !report) return null;

  const aiRecommendations = [
    "Contact local environmental authorities to report the issue",
    "Document the location with GPS coordinates for accurate reporting",
    "Take additional photos to show the extent of the problem",
    "Join local community groups focused on environmental protection"
  ];

  const handleReplyClick = () => {
    setIsReplying(!isReplying);
  };

  const handleReplySubmit = () => {
    if (replyText.trim()) {
      const newComment = {
        id: comments.length + 1,
        user: "You",
        text: replyText,
        avatar: "Y",
        timestamp: new Date().toLocaleString()
      };
      setComments([...comments, newComment]);
      setReplyText('');
      setIsReplying(false);
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
            {comments.map(comment => (
              <div key={comment.id} className="comment">
                <div className="comment-avatar">{comment.avatar}</div>
                <div className="comment-content">
                  <div className="comment-user">{comment.user}</div>
                  <div className="comment-text">{comment.text}</div>
                  <small>{comment.timestamp}</small>
                  <a href="#" className="comment-reply" onClick={handleReplyClick}>Reply</a>
                </div>
              </div>
            ))}
            {isReplying && (
              <div className="reply-section">
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  placeholder="Write your reply..."
                  rows="3"
                />
                <button onClick={handleReplySubmit} className="submit-reply-btn">Submit Reply</button>
                <button onClick={() => setIsReplying(false)} className="cancel-reply-btn">Cancel</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewReportModal;
