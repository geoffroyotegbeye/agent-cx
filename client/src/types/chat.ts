export interface Message {
  id: string;
  content: string;
  type: 'text' | 'voice';
  sender: 'user' | 'bot';
  timestamp: Date;
  status: 'Sending' | 'Send' | 'Delivered' | 'Read';
  audioUrl?: string;
}

export interface ChatState {
  messages: Message[];
  isTyping: boolean;
  searchQuery: string;
}