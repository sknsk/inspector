<template>
  <input
    type="checkbox"
    :class="[
      'h-4 w-4 rounded-sm border text-blue-600 focus:ring-blue-500',
      $attrs.class,
    ]"
    v-bind="attrsWithoutClass"
  />
</template>
<script setup lang="ts">
import { computed } from "vue";
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: cls, ...rest } = attrs;
  return rest;
});
</script>
