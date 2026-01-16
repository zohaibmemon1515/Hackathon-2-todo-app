export interface Conversation {
  id: number;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationSummary {
  id: number;
  title: string;
  lastUpdated: string;
}

export interface ConversationHistory {
  id: number;
  messages: Array<{
    role: string;
    content: string;
    timestamp: string;
  }>;
}