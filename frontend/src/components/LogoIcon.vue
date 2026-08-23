<template>
  <span class="logo-icon" :class="sizeClass">
    <img :src="logoSrc" :alt="ariaLabel" class="logo-image" />
  </span>
</template>

<script>
export default {
  name: 'LogoIcon',
  props: {
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
    },
    ariaLabel: {
      type: String,
      default: 'PDFhub'
    }
  },
  computed: {
    sizeClass() {
      return `logo-icon--${this.size}`
    },
    logoSrc() {
      return '/pdf-hub_logo.png'
    }
  }
}
</script>

<style scoped>
.logo-icon {
  display: inline-flex;
  align-items: center;
  line-height: 1;
  user-select: none;
}

.logo-icon--xs { width: 20px; height: 20px; }
.logo-icon--sm { width: 28px; height: 28px; }
.logo-icon--md { width: 36px; height: 36px; }
.logo-icon--lg { width: 44px; height: 44px; }
.logo-icon--xl { width: 64px; height: 64px; }

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>