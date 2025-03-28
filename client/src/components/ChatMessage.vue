<script setup lang="ts">
import { ref, computed } from 'vue';
import { format } from 'date-fns';
import type { Message } from '../types/chat';
import { UserCircleIcon, ComputerDesktopIcon } from '@heroicons/vue/24/solid';
import DOMPurify from "dompurify";


const props = defineProps<{
  message: Message;
}>();

const emit = defineEmits<{
  (e: 'edit', messageId: string, content: string): void;
}>();

const isEditing = ref(false);
const editedContent = ref(props.message.content);

const handleEdit = () => {
  if (isEditing.value) {
    emit('edit', props.message.id, editedContent.value);
  }
  isEditing.value = !isEditing.value;
};

// Déterminer si c'est un message de l'utilisateur ou du bot
const isUserMessage = computed(() => props.message.sender === 'user');
const formatText = (text: string) => {
  if (!text) return "";

  // Traiter les retours à la ligne entre les paragraphes
  text = text.replace(/\n\s*\n/g, "<p></p>");

  return text
    // Gras **texte**
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    // Italique *texte*
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    // Code `_texte_`
    .replace(/_(.*?)_/g, "<code>$1</code>")
    // Retours à la ligne simples
    .replace(/\n/g, "<br>")
    // Titres Markdown
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^# (.*)$/gm, "<h1>$1</h1>")
    // Si la ligne commence par un chiffre suivi d'un point (1., 2., 3., ...)
    .replace(/^(\d+\.)\s/gm, "<br><span>$1</span>") // On ajoute un <br> avant chaque numéro
    // Listes à puces avec des tirets ou des astérisques (- ou *)
    .replace(/^[\*\-]\s(.*)$/gm, "<ul><li>$1</li></ul>")
    // Ligne de tirets (------) forçant un retour à la ligne
    .replace(/^-{6,}$/gm, "<br>------<br>")
    // Sections avec "###", "##", "1.", etc., forçant à sauter une ligne au début
    .replace(/^(###|##|\d{1,2}\.)/gm, "<br>$&");
};

console.log(formatText(props.message.content));

</script>

<template>
  <div class="flex w-full mb-4 gap-3" :class="isUserMessage ? 'flex-row-reverse' : 'flex-row'">
    <div class="flex-shrink-0">
      <UserCircleIcon v-if="isUserMessage" class="h-8 w-8 text-gray-600 dark:text-gray-300" />
      <ComputerDesktopIcon v-else class="h-8 w-8 text-primary-600 dark:text-primary-400" />
    </div>

    <div :class="[ 'flex flex-col max-w-[70%] md:max-w-[60%]', isUserMessage ? 'items-end' : 'items-start' ]">
      <div :class="[ 
        'rounded-lg p-3 break-words text-start shadow', 
        isUserMessage 
          ? 'bg-blue-500 text-white rounded-tr-none'  // BLEU POUR L'UTILISATEUR
          : 'bg-gray-200 dark:bg-gray-700 text-gray-900  dark:text-gray-100 rounded-tl-none' // GRIS POUR L'IA
      ]">
        <div v-if="!isEditing" v-html="DOMPurify.sanitize(formatText(message.content))"></div>
        <input
          v-else
          v-model="editedContent"
          class="w-full bg-transparent border-b border-white focus:outline-none"
          @keyup.enter="handleEdit"
        />

        <!-- Affichage des messages audio -->
        <audio v-if="message.type === 'voice'" :src="message.audioUrl" controls class="mt-2 max-w-full"></audio>
      </div>

      <div class="flex items-center gap-3 mt-2 text-sm text-gray-600">
        <!-- Affichage de l'heure -->
        <span class="text-gray-500 p-2 bg-gray-200 rounded">
          Envoyé à {{ format(new Date(message.timestamp), 'HH:mm') }}
        </span>
        
        <!-- Bouton Edit/Save -->
        <button 
          v-if="isUserMessage"
          @click="handleEdit"
          class="text-blue-600 hover:text-blue-800 p-2 bg-blue-100 border:border-blue-100 text-xs font-semibold"
        >
          {{ isEditing ? 'Save' : 'Edit' }}
        </button>
        
        <!-- Statut du message -->
        <span v-if="isUserMessage" class="text-xs text-gray-800 p-2 bg-red-200 rounded">
          {{ message.status }}
        </span>
      </div>

    </div>
  </div>
</template>
