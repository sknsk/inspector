<template>
  <label
    :for="forId"
    :class="['text-sm font-medium', $attrs.class]"
    v-bind="attrsWithoutClass"
    ><slot
  /></label>
</template>
<script setup lang="ts">
import { computed } from "vue";
const props = defineProps<{ forId?: string }>();
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: cls, ...rest } = attrs;
  return rest;
});
</script>
