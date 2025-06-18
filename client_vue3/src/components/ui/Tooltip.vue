<template>
  <span class="relative" @mouseenter="show = true" @mouseleave="show = false">
    <slot />
    <span
      v-if="show"
      class="absolute z-10 -top-6 left-1/2 -translate-x-1/2 rounded bg-gray-700 text-white text-xs px-2 py-1"
    >
      {{ text }}
    </span>
  </span>
</template>
<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{ text: string }>();
const show = ref(false);
</script>
