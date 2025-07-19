import os
from dotenv import load_dotenv

# LangChain imports for cleaner code
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self, document_service=None):
        """Initialize the AI service with LangChain Gemini."""
        # Get API key from environment variable (secure)
        self.api_key = os.environ.get('GOOGLE_API_KEY', 'AIzaSyC2tznCdJX-y9YzEuE_USCA3BVUuo1-av4')
        self.model_name = "gemini-1.5-flash-latest"
        
        # LangChain Gemini chat model - much cleaner!
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Store reference to document service for embedding search
        self.document_service = document_service
        
    def query_documents(self, query, document_type, chat_history=None, context_message="", is_first_message=False):
        """
        Query documents of a specific type using RAG with PostgreSQL embeddings.
        
        Args:
            query (str): The user query
            document_type (str): The type of document to search (Case Section Analysis, Bail Analysis, Human Analysis)
            chat_history (list): List of previous conversations as (question, answer) tuples
            context_message (str): Context message for the conversation
            is_first_message (bool): Whether this is the first message in the conversation
            
        Returns:
            str: The AI response
        """
        # Initialize chat history if None
        if chat_history is None:
            chat_history = []
        
        try:
            # Get relevant document chunks using advanced semantic search
            if self.document_service:
                print(f"DEBUG: Searching for query: '{query}' with document_type: '{document_type}'")
                
                # First check if any documents exist
                all_docs = self.document_service.get_all_documents()
                print(f"DEBUG: Total documents in database: {len(all_docs)}")
                for doc in all_docs[:5]:  # Show first 5
                    print(f"  - {doc.document_name} (Type: {doc.document_type})")
                
                search_results = self.document_service.semantic_search_chunks(
                    query=query,
                    document_type=document_type,
                    limit=5,
                    similarity_threshold=0.2  # Even lower threshold for testing
                )
                print(f"DEBUG: Search returned {len(search_results) if search_results else 0} results")
                
                # If no results with document type filter, try without filter
                if not search_results and document_type:
                    print(f"DEBUG: No results with document_type '{document_type}', trying without filter")
                    search_results = self.document_service.semantic_search_chunks(
                        query=query,
                        document_type=None,  # No filter
                        limit=5,
                        similarity_threshold=0.1  # Very low threshold
                    )
                    print(f"DEBUG: Search without filter returned {len(search_results) if search_results else 0} results")
                
                # Extract text content and prepare source references
                if search_results:
                    context_parts = []
                    source_references = []
                    
                    for i, result in enumerate(search_results, 1):
                        chunk_text = result['chunk_text']
                        doc_name = result['document_name']
                        similarity = result['final_score']  # Use enhanced score
                        chunk_id = result['chunk_id']
                        relevance_reason = result.get('relevance_reason', '')
                        
                        context_parts.append(f"[Source {i}]: {chunk_text}")
                        source_references.append({
                            'id': i,
                            'chunk_id': chunk_id,
                            'document_name': doc_name,
                            'similarity': f"{similarity:.2%}",
                            'preview': result['preview'],
                            'document_id': result['document_id'],
                            'relevance_reason': relevance_reason
                        })
                    
                    context = "\n\n".join(context_parts)
                    
                    # Store source references for UI (you'll need to pass this to the template)
                    self._last_sources = source_references
                    print(f"DEBUG: Generated {len(source_references)} source references") # Debug log
                else:
                    # Check if any documents exist at all
                    total_docs = len(self.document_service.get_all_documents()) if self.document_service else 0
                    if total_docs == 0:
                        context = "No documents have been uploaded to the system yet. Please upload relevant documents to get answers based on your files."
                    else:
                        context = f"No relevant documents found for this query in your {total_docs} uploaded files. The query might be too specific or the documents may not contain related information."
                    self._last_sources = []
                    print("DEBUG: No search results found") # Debug log
            else:
                context = "Document search service not available. Cannot access uploaded documents."
                self._last_sources = []
            
            # Build chat history context
            history_context = ""
            if chat_history:
                history_context = "\n\nPrevious conversation:\n"
                for q, a in chat_history[-3:]:  # Last 3 exchanges
                    history_context += f"Q: {q}\nA: {a}\n"
            
            # Create appropriate prompt based on whether it's the first message
            if is_first_message:
                # For first message, provide a welcoming response with context
                if context_message:
                    if query.lower() in ['hi', 'hello', 'hey', 'start']:
                        # Simple greeting
                        prompt = f"""You are an AI assistant specializing in legal analysis for police cases. You can ONLY provide information based on the documents uploaded to this system.

{context_message}

The user has greeted you with: "{query}"

Please respond with a warm, professional greeting and explain that you can help them analyze their uploaded legal documents. Emphasize that you will only use information from their uploaded documents, not from the internet or general knowledge."""
                    else:
                        # First message with actual question
                        prompt = f"""You are an AI assistant specializing in legal analysis for police cases. You can ONLY answer questions using information from the uploaded documents provided below. Do NOT use any information from the internet, general knowledge, or external sources.

{context_message}

IMPORTANT: Base your answer ONLY on the following document excerpts. If the EXACT information is not found but RELATED information exists, explain what you found and how it relates to the question.

Context from uploaded documents:
{context}

User's question: "{query}"

Instructions:
1. Only use information from the document excerpts above
2. If the exact answer is not in the documents but related information exists, explain what you found
3. If NO related information exists at all, say "This information is not available in your uploaded documents"
4. Always cite which source you're referencing (e.g., "According to Source 1...")
5. Be helpful by explaining what information IS available, even if it's not a perfect match to every detail in the question
6. Do not add any external knowledge or internet information"""
                else:
                    # Fallback for first message
                    prompt = f"""You are an AI assistant for police case analysis. You can ONLY provide information from uploaded documents.

IMPORTANT: Base your answer ONLY on the following document excerpts. Do NOT use external knowledge.

Context from uploaded documents:
{context}

Question: "{query}"

If this is a greeting, respond warmly. For questions, only use the document context provided above. If information is not in the documents, clearly state this."""
            else:
                # For subsequent messages, use the strict format
                prompt = f"""You are an AI assistant specializing in police case analysis. You can ONLY answer questions using information from the uploaded documents provided below. Do NOT use any information from the internet, general knowledge, or external sources.

CRITICAL INSTRUCTIONS:
1. ONLY use information from the document excerpts below
2. Do NOT add any external knowledge, internet information, or general legal knowledge
3. If the EXACT answer is not in the provided documents, but RELATED information exists, acknowledge the related information and explain what you found
4. If NO related information exists, say "This information is not available in your uploaded documents"
5. Always reference sources when providing information (e.g., "According to Source 1...")
6. If the user asks about specific amendments or provisions, look for related legal provisions even if they don't match exactly
7. Be helpful by explaining what information IS available, even if it's not a perfect match

Context from uploaded documents:
{context}
{history_context}

User's question: "{query}"

IMPORTANT: If you find related information in the sources (even if not an exact match), explain what you found and how it relates to the question. Don't dismiss relevant information just because it doesn't match every detail of the query."""

            # Generate response using LangChain - with strict document-only instructions
            messages = [
                SystemMessage(content="""You are an AI assistant for police case analysis. CRITICAL RULES:
1. ONLY use information from the document excerpts provided in the user's message
2. NEVER use external knowledge, internet information, or general legal knowledge
3. If EXACT information is not in the provided documents but RELATED information exists, explain what you found and how it relates
4. If NO related information exists at all, clearly state it's not available
5. Always cite sources when referencing information
6. Be helpful by explaining what information IS available, even if it doesn't match every detail of the query
7. Stay strictly within the bounds of the uploaded document context"""),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Format response to add source references to UI
            import re
            formatted_response = re.sub(
                r'\b([Ss]ource\s+(\d+))\b',
                r'<span class="source-citation" data-source-id="\2">\1</span>',
                response.content
            )
            
            # Return both response and sources for UI
            result = {
                'response': formatted_response,
                'sources': getattr(self, '_last_sources', [])
            }
            print(f"DEBUG: Returning response with {len(result['sources'])} sources") # Debug log
            return result
            
        except Exception as e:
            print(f"Error in query_documents: {e}")
            return self.direct_query(query)
    
    def direct_query(self, prompt):
        """
        Direct query to Gemini using LangChain.
        
        Args:
            prompt (str): The prompt to send to Gemini
            
        Returns:
            str: The AI response
        """
        try:
            # LangChain makes this super easy!
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in direct_query: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    def get_last_sources(self):
        """Get the sources from the last query for UI display."""
        return getattr(self, '_last_sources', [])
    
    def get_chunk_context(self, chunk_id, context_size=500):
        """
        Get expanded context around a specific chunk for highlighting.
        
        Args:
            chunk_id (int): The chunk ID to get context for
            context_size (int): Number of characters before/after to include
            
        Returns:
            dict: Chunk info with expanded context
        """
        if not self.document_service:
            return None
            
        try:
            from app.models.database import Chunk, Document
            from sqlalchemy import text
            
            # Get the chunk and surrounding chunks
            sql = """
            SELECT 
                c.chunk_id,
                c.chunk_text,
                c.chunk_order,
                d.document_name,
                d.document_type,
                d.document_id,
                d.file_path
            FROM chunks c
            JOIN documents d ON c.document_id = d.document_id
            WHERE c.chunk_id = %s
            """
            
            result = self.document_service.db_session.execute(text(sql), [chunk_id])
            row = result.fetchone()
            
            if not row:
                return None
                
            # Get surrounding chunks for better context
            surrounding_sql = """
            SELECT chunk_text, chunk_order
            FROM chunks 
            WHERE document_id = (SELECT document_id FROM chunks WHERE chunk_id = %s)
            AND chunk_order BETWEEN 
                (SELECT chunk_order - 2 FROM chunks WHERE chunk_id = %s) AND 
                (SELECT chunk_order + 2 FROM chunks WHERE chunk_id = %s)
            ORDER BY chunk_order
            """
            
            surrounding_result = self.document_service.db_session.execute(
                text(surrounding_sql), [chunk_id, chunk_id, chunk_id]
            )
            
            surrounding_chunks = [r.chunk_text for r in surrounding_result]
            expanded_context = " ".join(surrounding_chunks)
            
            return {
                'chunk_id': row.chunk_id,
                'chunk_text': row.chunk_text,
                'expanded_context': expanded_context,
                'document_name': row.document_name,
                'document_type': row.document_type,
                'document_id': row.document_id,
                'file_path': row.file_path
            }
            
        except Exception as e:
            print(f"Error getting chunk context: {e}")
            return None
    
    def _format_response_with_sources(self, response_text):
        """
        Format response text to add clickable source references.
        
        Args:
            response_text (str): The raw response text from the model
            
        Returns:
            str: HTML formatted response with clickable source references
        """
        import re
        
        # Replace source references with clickable spans
        # Pattern matches "Source X" or "source X" where X is a number
        pattern = r'\b([Ss]ource\s+(\d+))\b'
        
        # Replace with HTML span element for source citation
        formatted_text = re.sub(
            pattern, 
            r'<span class="source-citation" data-source-id="\2">\1</span>', 
            response_text
        )
        
        return formatted_text
