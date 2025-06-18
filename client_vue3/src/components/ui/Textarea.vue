<template>
  <textarea
    :rows="rows"
    :class="[
      'flex w-full rounded-md border px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50',
      $attrs.class,
    ]"
    v-bind="attrsWithoutClass"
  ></textarea>
</template>
<script setup lang="ts">
import { computed } from "vue";
const props = withDefaults(defineProps<{ rows?: number }>(), { rows: 3 });
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: cls, ...rest } = attrs;
  return rest;
});
</script>
