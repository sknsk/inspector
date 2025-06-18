<template>
  <v-btn
    :color="color"
    :variant="variantProp"
    :size="sizeProp"
    v-bind="attrsWithoutClass"
  >
    <slot />
  </v-btn>
</template>

<script setup lang="ts">
import { computed, useAttrs } from "vue";
import { VBtn } from "vuetify/components";

const props = withDefaults(defineProps<{ variant?: string; size?: string }>(), {
  variant: "default",
  size: "default",
});
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: _cls, ...rest } = attrs as any;
  return rest;
});

const color = computed(() => {
  if (props.variant === "destructive") return "red";
  if (props.variant === "secondary") return "grey";
  return "primary";
});

const variantProp = computed(() => {
  if (props.variant === "outline") return "outlined";
  if (props.variant === "ghost" || props.variant === "link") return "text";
  return "elevated";
});

const sizeProp = computed(() => {
  if (props.size === "sm") return "small";
  if (props.size === "lg") return "large";
  return "default";
});
</script>
