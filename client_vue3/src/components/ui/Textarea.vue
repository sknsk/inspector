<template>
  <v-textarea v-model="model" :rows="rows" v-bind="attrsWithoutClass" />
</template>

<script setup lang="ts">
import { computed, useAttrs } from "vue";
import { VTextarea } from "vuetify/components";

const props = withDefaults(defineProps<{ modelValue?: any; rows?: number }>(), {
  rows: 3,
});
const emit = defineEmits(["update:modelValue"]);
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: _cls, ...rest } = attrs as any;
  return rest;
});

const model = computed({
  get: () => props.modelValue,
  set: (v) => emit("update:modelValue", v),
});
</script>
