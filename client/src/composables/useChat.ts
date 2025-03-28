import { ref, computed } from 'vue';
import { useStorage } from '@vueuse/core';
import type { Message, ChatState } from '../types/chat';

export function useChat() {
  const state = useStorage<ChatState>('chat-state', {
    messages: [],
    isTyping: false,
    searchQuery: '',
  });

  const filteredMessages = computed(() => {
    if (!state.value.searchQuery) return state.value.messages;
    return state.value.messages.filter(message => 
      message.content.toLowerCase().includes(state.value.searchQuery.toLowerCase())
    );
  });

  const addMessage = async (content: string, type: 'text' | 'voice' = 'text', audioUrl?: string) => {
    const message: Message = {
      id: Date.now().toString(),
      content,
      type,
      sender: 'user',
      timestamp: new Date(),
      status: 'sending',
      audioUrl,
    };

    state.value.messages.push(message);
    
    // Mettre à jour le statut du message
    setTimeout(() => {
      message.status = 'sent';
      setTimeout(() => {
        message.status = 'delivered';
        setTimeout(() => {
          message.status = 'read';
        }, 500);
      }, 500);
    }, 500);

    // 🔹 Communication avec le backend
    state.value.isTyping = true;
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: content }),
      });

      const data = await response.json();
      console.log(data.response.content);

      if (response.ok) {
        const botMessage: Message = {
          id: Date.now().toString(),
          content: data.response, // La réponse renvoyée par le backend
          type: 'text',
          sender: 'bot',
          timestamp: new Date(),
          status: 'read',
        };
        state.value.messages.push(botMessage);
      } else {
        console.error('Erreur API:', data);
        console.log(data.response); // Vérifie ce qui est renvoyé par le backend
      }
    } catch (error) {
      console.error('Erreur de connexion au serveur:', error);
    } finally {
      state.value.isTyping = false;
    }
  };

  const editMessage = (messageId: string, newContent: string) => {
    const index = state.value.messages.findIndex(m => m.id === messageId);
    if (index !== -1) {
      state.value.messages[index].content = newContent;
      state.value.messages = state.value.messages.slice(0, index + 1);
      state.value.isTyping = true;
      setTimeout(() => {
        addMessage(newContent);
      }, 500);
    }
  };

  const setSearchQuery = (query: string) => {
    state.value.searchQuery = query;
  };

  return {
    messages: computed(() => state.value.messages),
    filteredMessages,
    isTyping: computed(() => state.value.isTyping),
    searchQuery: computed(() => state.value.searchQuery),
    addMessage,
    editMessage,
    setSearchQuery,
  };
}
