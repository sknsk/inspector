<template>
  <div class="relative inline-block" ref="wrapper">
    <slot name="trigger" />
    <div
      v-if="open"
      class="absolute z-10 mt-1 rounded-md border bg-white p-2 shadow"
      @click="open = false"
    >
      <slot />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
const open = ref(false);
const wrapper = ref<HTMLElement | null>(null);
</script>
