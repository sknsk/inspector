<template>
  <dialog
    ref="dialog"
    :open="open"
    class="rounded-md p-4 bg-white shadow-md"
    v-bind="attrsWithoutClass"
  >
    <slot />
  </dialog>
</template>
<script setup lang="ts">
import { ref, watch, computed } from "vue";
const props = withDefaults(defineProps<{ open?: boolean }>(), { open: false });
const dialog = ref<HTMLDialogElement | null>(null);
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: cls, ...rest } = attrs;
  return rest;
});
watch(
  () => props.open,
  (val) => {
    if (!dialog.value) return;
    if (val) dialog.value.showModal();
    else dialog.value.close();
  },
);
</script>
