import { ref } from 'vue';

export function useAudioRecording() {
  const isRecording = ref(false);
  const audioURL = ref<string | null>(null);
  const mediaRecorder = ref<MediaRecorder | null>(null);
  const audioChunks = ref<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.value = new MediaRecorder(stream);
      audioChunks.value = [];

      mediaRecorder.value.ondataavailable = (event) => {
        audioChunks.value.push(event.data);
      };

      mediaRecorder.value.onstop = () => {
        const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' });
        audioURL.value = URL.createObjectURL(audioBlob);
      };

      mediaRecorder.value.start();
      isRecording.value = true;
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.value && isRecording.value) {
      mediaRecorder.value.stop();
      isRecording.value = false;
      mediaRecorder.value.stream.getTracks().forEach(track => track.stop());
    }
  };

  return {
    isRecording,
    audioURL,
    startRecording,
    stopRecording,
  };
}