<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50',
      variantClass,
      sizeClass,
      $attrs.class,
    ]"
    v-bind="attrsWithoutClass"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";
const props = withDefaults(defineProps<{ variant?: string; size?: string }>(), {
  variant: "default",
  size: "default",
});
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: cls, ...rest } = attrs;
  return rest;
});
const variantClass = computed(() => {
  switch (props.variant) {
    case "destructive":
      return "bg-red-600 text-white hover:bg-red-500";
    case "outline":
      return "border border-gray-300";
    case "secondary":
      return "bg-gray-200";
    case "ghost":
      return "bg-transparent";
    case "link":
      return "underline text-blue-600";
    default:
      return "bg-blue-600 text-white hover:bg-blue-500";
  }
});
const sizeClass = computed(() => {
  switch (props.size) {
    case "sm":
      return "h-8 px-3 text-xs";
    case "lg":
      return "h-10 px-8";
    case "icon":
      return "h-9 w-9 p-0";
    default:
      return "h-9 px-4";
  }
});
</script>
