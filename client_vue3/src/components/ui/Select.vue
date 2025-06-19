<template>
  <select
    :class="[
      'h-9 rounded-md border bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500',
      $attrs.class,
    ]"
    v-bind="attrsWithoutClass"
  >
    <slot />
  </select>
</template>
<script setup lang="ts">
import { computed } from "vue";
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: cls, ...rest } = attrs;
  return rest;
});
</script>
