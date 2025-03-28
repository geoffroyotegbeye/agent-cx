<script setup lang="ts">
import { ref } from 'vue';
import { useChat } from './composables/useChat';
import { useDark, useToggle } from '@vueuse/core';
import ChatMessage from './components/ChatMessage.vue';
import ChatInput from './components/ChatInput.vue';
import { MoonIcon, SunIcon, MagnifyingGlassIcon } from '@heroicons/vue/24/solid';

const isDark = useDark();
const toggleDark = useToggle(isDark);
const { messages, isTyping, filteredMessages, addMessage, editMessage, setSearchQuery } = useChat();
const searchVisible = ref(false);
</script>

<template>
  <div class="h-[70vh] bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <div class="mx-auto h-[800px] flex flex-col md:max-w-4xl w-full position: relative bottom-20">
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b dark:border-gray-700">
        <h1 class="text-xl font-bold font-serif text-blue-500 p-2 bg-gray-200 rounded-lg">INSPECTOR IA CHATBOOT 🤖 </h1>
        <div class="flex items-center gap-4">
          <button @click="searchVisible = !searchVisible" class="p-2">
            <MagnifyingGlassIcon class="h-6 w-6" />
          </button>
          <button @click="toggleDark()" class="p-2">
            <MoonIcon v-if="!isDark" class="h-6 w-6" />
            <SunIcon v-else class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Search Bar -->
      <div v-if="searchVisible" class="p-4 border-b dark:border-gray-700">
        <input
          type="text"
          placeholder="Search messages..."
          class="w-full bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
          @input="e => setSearchQuery((e.target as HTMLInputElement).value)"
        />
      </div>

      <!-- Chat Messages -->
      <div class="flex-1 overflow-y-auto p-4">
        <ChatMessage
          v-for="message in filteredMessages"
          :key="message.id"
          :message="message"
          @edit="editMessage"
        />
        <div v-if="isTyping" class="flex items-center gap-2 text-gray-500">
          <span class="animate-bounce">•</span>
          <span class="animate-bounce delay-100">•</span>
          <span class="animate-bounce delay-200">•</span>
        </div>
      </div>

      <!-- Chat Input -->
      <footer class="mx-10 mb-16">
        <ChatInput @send="addMessage" />
      </footer>
    </div>
  </div>
</template>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Mobile-first responsive design */
@media (max-width: 768px) {
  .max-w-3xl {
    max-width: 100%;
  }
}
</style>