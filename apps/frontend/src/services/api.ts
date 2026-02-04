/**
 * API service for chat functionality
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL + "/api/v1";

interface SendMessageRequest {
  message: string;
  conversation_id?: string;
}

interface SendMessageResponse {
  response: string;
  conversation_id: string;
  message_id?: string;
}

/**
 * Send a message to the chat endpoint
 */
export const sendMessage = async (
  userId: string,
  message: string,
  conversationId?: string
): Promise<SendMessageResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

/**
 * Get user conversations
 */
export const getUserConversations = async (userId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations?user_id=${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // FIX: Sirf conversations array return karein, pura object nahi
    // Isse 'conversations.map is not a function' error khatam ho jayega
    return data.conversations || []; 
    
  } catch (error) {
    console.error('Error fetching conversations:', error);
    return []; // Error par empty array return karein taaki frontend crash na ho
  }
};

/**
 * Get conversation details
 */
export const getConversationDetails = async (conversationId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // FIX: Agar messages backend se wrap hoke aa rahe hain toh unhe extract karein
    return data.messages || data; 
    
  } catch (error) {
    console.error('Error fetching conversation details:', error);
    throw error;
  }
};