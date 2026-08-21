<template>
  <span class="logo-icon" :class="sizeClass">
    <span class="logo-text-pdf">PDF</span>
    <strong class="logo-text-hub">hub</strong>
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
    }
  },
  computed: {
    sizeClass() {
      return `logo-icon--${this.size}`
    }
  }
}
</script>

<style scoped>
.logo-icon {
  display: inline-flex;
  align-items: center;
  font-weight: 900;
  letter-spacing: -0.09em;
  line-height: 1;
  user-select: none;
}

.logo-icon--xs { font-size: 12px; }
.logo-icon--sm { font-size: 16px; }
.logo-icon--md { font-size: 20px; }
.logo-icon--lg { font-size: 28px; }
.logo-icon--xl { font-size: 40px; }

.logo-text-pdf { color: #f5f5f5; }

.logo-text-hub {
  margin-left: 0.15em;
  padding: 0.15em 0.25em 0.18em;
  border-radius: 0.14em;
  background: #FF9F1C;
  color: #111;
  letter-spacing: -0.08em;
}
</style>