<script setup lang="ts">
import { ref } from 'vue';
import { MicrophoneIcon, PaperAirplaneIcon } from '@heroicons/vue/24/solid';
import { useAudioRecording } from '../composables/useAudioRecording';

const emit = defineEmits<{
  (e: 'send', content: string, type: 'text' | 'voice', audioUrl?: string): void;
}>();

const message = ref('');
const { isRecording, audioURL, startRecording, stopRecording } = useAudioRecording();

const sendMessage = () => {
  if (message.value.trim()) {
    emit('send', message.value, 'text');
    message.value = '';
  }
};

const handleVoiceMessage = async () => {
  if (isRecording.value) {
    stopRecording();
    if (audioURL.value) {
      emit('send', 'Voice message', 'voice', audioURL.value);
    }
  } else {
    await startRecording();
  }
};
</script>

<template>
  <div class="flex items-center gap-2 bg-white dark:bg-gray-800 p-4 border-t dark:border-gray-700">
    <input
      v-model="message"
      type="text"
      placeholder="Type your message..."
      class="flex-1 bg-gray-100 dark:bg-gray-700 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
      @keyup.enter="sendMessage"
    />
    
    <button
      @click="handleVoiceMessage"
      :class="[
        'p-2 rounded-full',
        isRecording 
          ? 'bg-red-500 text-white' 
          : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
      ]"
    >
      <MicrophoneIcon class="h-5 w-5" />
    </button>
    
    <button
      @click="sendMessage"
      class="p-2 rounded-full bg-primary-500 text-white disabled:opacity-50 disabled:cursor-not-allowed"
      :disabled="!message.trim()"
    >
      <PaperAirplaneIcon class="h-5 w-5" />
    </button>
  </div>
</template>
