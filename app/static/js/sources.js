// Source of Truth highlighting and document display
document.addEventListener('DOMContentLoaded', function() {
  // Handle source citation clicks
  document.addEventListener('click', function(e) {
    if (e.target && e.target.matches('.source-citation')) {
      e.preventDefault();
      console.log('Source citation clicked!'); // Debug log
      
      const sourceId = e.target.getAttribute('data-source-id');
      const sourceDataId = e.target.getAttribute('data-source-data-id');
      console.log('Source ID:', sourceId, 'Source Data ID:', sourceDataId); // Debug log
      
      // Find source data using the specific ID or fallback to class search
      let sourceDataElement = null;
      if (sourceDataId) {
        sourceDataElement = document.getElementById(sourceDataId);
      }
      
      if (!sourceDataElement) {
        // Fallback: find in the same message container
        const messageContainer = e.target.closest('.message');
        sourceDataElement = messageContainer ? messageContainer.querySelector('.source-data') : document.querySelector('.source-data');
      }
      
      if (sourceDataElement) {
        const sourceData = JSON.parse(sourceDataElement.getAttribute('data-sources'));
        console.log('Source data found:', sourceData); // Debug log
        
        if (sourceData && sourceData[sourceId-1]) {
          showSourceHighlight(sourceData[sourceId-1]);
        } else {
          console.log('Source not found in data array');
        }
      } else {
        console.log('Source data element not found');
      }
    }
  });
});

// Show source highlight modal with the highlighted text
function showSourceHighlight(source) {
  // Create modal if it doesn't exist
  let modal = document.getElementById('source-modal');
  
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'source-modal';
    modal.className = 'source-modal';
    
    const modalContent = document.createElement('div');
    modalContent.className = 'source-modal-content';
    
    const closeBtn = document.createElement('span');
    closeBtn.className = 'source-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.onclick = closeSourceModal;
    
    const modalHeader = document.createElement('div');
    modalHeader.className = 'source-modal-header';
    
    const modalBody = document.createElement('div');
    modalBody.className = 'source-modal-body';
    modalBody.id = 'source-content';
    
    modalHeader.appendChild(closeBtn);
    modalContent.appendChild(modalHeader);
    modalContent.appendChild(modalBody);
    modal.appendChild(modalContent);
    
    document.body.appendChild(modal);
  }
  
  // Update modal content with source information
  const modalBody = document.getElementById('source-content');
  
  let content = `
    <h3>Source: ${source.document_name}</h3>
    <div class="source-meta">
      <span class="source-relevance">Relevance: ${source.similarity}</span>
      ${source.relevance_reason ? `<br><small class="relevance-reason">${source.relevance_reason}</small>` : ''}
    </div>
    <div class="source-text">
      ${highlightSourceText(source.preview)}
    </div>
  `;
  
  modalBody.innerHTML = content;
  modal.style.display = 'block';
}

// Highlight key terms in the source text
function highlightSourceText(text) {
  // Get the last user query from chat
  const lastQuery = document.querySelector('.chat-message.user:last-child .message-text');
  if (!lastQuery) return text;
  
  const queryText = lastQuery.textContent;
  const keywords = extractKeywords(queryText);
  
  let highlightedText = text;
  
  keywords.forEach(keyword => {
    if (keyword.length > 3) { // Only highlight meaningful keywords
      const regex = new RegExp(`(${keyword})`, 'gi');
      highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
    }
  });
  
  return highlightedText;
}

// Extract keywords from query
function extractKeywords(query) {
  // Simple keyword extraction - remove common words
  const stopWords = ['the', 'and', 'or', 'in', 'on', 'at', 'to', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'this', 'that'];
  return query.toLowerCase()
    .replace(/[^\w\s]/g, '')
    .split(/\s+/)
    .filter(word => !stopWords.includes(word));
}

// Close the source modal
function closeSourceModal() {
  document.getElementById('source-modal').style.display = 'none';
}

// Format AI response with source citations
function formatWithSourceCitations(text) {
  // Replace "Source X" mentions with clickable citations
  return text.replace(/\b(Source\s+(\d+))\b/gi, '<a href="#" class="source-citation" data-source-id="$2">$1</a>');
}
