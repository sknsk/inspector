<template>
  <div
    :class="[
      'relative w-full rounded-lg border px-4 py-3 text-sm',
      variant === 'destructive' ? 'border-red-600 text-red-600' : 'bg-white',
      $attrs.class,
    ]"
    v-bind="attrsWithoutClass"
  >
    <slot />
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
const props = withDefaults(
  defineProps<{ variant?: "default" | "destructive" }>(),
  { variant: "default" },
);
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: c, ...rest } = attrs;
  return rest;
});
</script>
