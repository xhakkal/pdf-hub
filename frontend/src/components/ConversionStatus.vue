<template>
  <div class="conversion-status" v-if="isVisible">
    <!-- Loading State -->
    <div v-if="status === 'loading'" class="status-container loading">
      <!-- Animated Spinner Ring -->
      <div class="spinner-wrapper">
        <div class="spinner-ring"></div>
        <div class="spinner-ring spinner-ring--2"></div>
        <div class="spinner-ring spinner-ring--3"></div>
        <div class="spinner-center">
          <svg class="spinner-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </div>
      </div>

      <!-- Status Text with Animation -->
      <p class="status-text">
        <span class="text-main">Processando seu arquivo</span>
        <span class="text-dots" v-if="progress < 100">
          <span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
        </span>
      </p>

      <!-- Progress Bar -->
      <div class="progress-info" v-if="progress > 0">
        <div class="progress-bar" role="progressbar" :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
          <div
            class="progress-fill"
            :style="{ width: progress + '%' }"
            :class="{ 'progress-fill--complete': progress >= 100 }"
          >
            <div class="progress-shine"></div>
          </div>
        </div>

        <div class="progress-details">
          <span class="progress-percent">{{ progressRounded }}%</span>
          <span class="progress-time" v-if="estimatedTime">⏱ ~{{ estimatedTime }}s restantes</span>
        </div>

        <!-- Step indicator -->
        <div class="progress-steps" v-if="progress > 0">
          <div
            v-for="(step, index) in processingSteps"
            :key="index"
            :class="['step', { 'step--active': index <= currentStepIndex, 'step--done': index < currentStepIndex }]"
          >
            <div class="step-indicator">
              <span v-if="index < currentStepIndex" class="step-check">✓</span>
              <span v-else-if="index === currentStepIndex" class="step-pulse"></span>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="step-label">{{ step }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Success State -->
    <div v-if="status === 'success'" class="status-container success">
      <div class="success-animation">
        <div class="success-ring"></div>
        <div class="success-ring success-ring--2"></div>
        <svg class="success-checkmark" viewBox="0 0 52 52">
          <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
          <path class="checkmark-path" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
        </svg>
      </div>
      <p class="status-text">Conversão concluída com sucesso!</p>
      <p class="status-subtext">Seu arquivo está pronto para download</p>
      <button @click="$emit('close')" class="status-button success-button">Fechar</button>
    </div>

    <!-- Error State -->
    <div v-if="status === 'error'" class="status-container error">
      <div class="error-animation">
        <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" stroke-width="2"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4M12 16h.01" />
        </svg>
      </div>
      <p class="status-text">Erro na conversão</p>
      <p class="status-subtext error-message">{{ errorMessage }}</p>
      <button @click="$emit('close')" class="status-button error-button">Tentar novamente</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConversionStatus',
  props: {
    status: {
      type: String,
      required: true,
      validator: (value) => ['idle', 'loading', 'success', 'error'].includes(value)
    },
    errorMessage: {
      type: String,
      default: 'Ocorreu um erro durante a conversão'
    },
    progress: {
      type: Number,
      default: 0
    },
    estimatedTime: {
      type: Number,
      default: null
    }
  },
  computed: {
    isVisible() {
      return this.status !== 'idle'
    },
    progressRounded() {
      return Math.round(this.progress)
    },
    processingSteps() {
      return [
        'Enviando arquivo',
        'Processando',
        'Gerando resultado',
        'Preparando download'
      ]
    },
    currentStepIndex() {
      if (this.progress < 25) return 0
      if (this.progress < 50) return 1
      if (this.progress < 75) return 2
      return 3
    }
  }
}
</script>

<style scoped>
.conversion-status {
  width: 100%;
  margin-top: 24px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.status-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 28px 24px;
  border-radius: 16px;
  text-align: center;
  border: 2px solid;
  position: relative;
  overflow: hidden;
}

/* Loading Styles */
.status-container.loading {
  background: linear-gradient(135deg, rgba(255, 159, 28, 0.08), rgba(255, 159, 28, 0.03));
  border-color: #FF9F1C;
  color: #fff;
}

/* Spinner Animation */
.spinner-wrapper {
  position: relative;
  width: 72px;
  height: 72px;
}

.spinner-ring {
  position: absolute;
  inset: 0;
  border: 3px solid transparent;
  border-top-color: #FF9F1C;
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.spinner-ring--2 {
  animation-duration: 1.8s;
  animation-direction: reverse;
  border-top-color: #FFB84D;
  inset: 8px;
}

.spinner-ring--3 {
  animation-duration: 2.4s;
  border-top-color: #FFD180;
  inset: 16px;
}

.spinner-center {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner-icon {
  width: 28px;
  height: 28px;
  color: #FF9F1C;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
}

/* Status Text */
.status-text {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.01em;
}

.text-dots {
  display: inline-block;
  width: 1.2em;
  text-align: left;
  animation: dots 1.5s steps(3) infinite;
}

@keyframes dots {
  0%, 20% { width: 0; }
  40% { width: 0.4em; }
  60% { width: 0.8em; }
  80%, 100% { width: 1.2em; }
}

/* Progress Bar */
.progress-info {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 4px;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: rgba(255, 159, 28, 0.15);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF9F1C, #FFB84D, #FFD180);
  background-size: 200% 100%;
  border-radius: 6px;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  animation: gradientShift 2s ease infinite;
}

.progress-fill--complete {
  animation: none;
  background: linear-gradient(90deg, #22C55E, #4ADE80);
}

.progress-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shine 1.5s ease-in-out infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-details {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #888;
  padding: 0 4px;
}

.progress-percent {
  font-weight: 700;
  color: #FF9F1C;
  font-variant-numeric: tabular-nums;
}

.progress-time {
  opacity: 0.8;
  font-variant-numeric: tabular-nums;
}

/* Progress Steps */
.progress-steps {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 400px;
  margin-top: 8px;
  padding: 0 4px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
  position: relative;
}

.step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 10px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: rgba(255, 159, 28, 0.15);
  z-index: 0;
}

.step-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #fff;
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
  z-index: 1;
  transition: all 0.3s ease;
}

.step--active .step-indicator {
  background: #FF9F1C;
  border-color: #FF9F1C;
  box-shadow: 0 0 0 4px rgba(255, 159, 28, 0.2);
}

.step--done .step-indicator {
  background: #22C55E;
  border-color: #22C55E;
}

.step-pulse {
  width: 8px;
  height: 8px;
  background: #FF9F1C;
  border-radius: 50%;
  animation: stepPulse 1s ease-in-out infinite;
}

@keyframes stepPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.6; }
}

.step-check {
  color: #fff;
  font-size: 10px;
}

.step-label {
  font-size: 10px;
  color: #666;
  white-space: nowrap;
  text-align: center;
  max-width: 80px;
}

.step--active .step-label {
  color: #FF9F1C;
  font-weight: 600;
}

.step--done .step-label {
  color: #22C55E;
}

/* Success Styles */
.status-container.success {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.04));
  border-color: #22C55E;
}

.success-animation {
  position: relative;
  width: 80px;
  height: 80px;
}

.success-ring {
  position: absolute;
  inset: 0;
  border: 3px solid transparent;
  border-top-color: #22C55E;
  border-radius: 50%;
  animation: successRing 1.5s ease-out forwards;
}

.success-ring--2 {
  animation-delay: 0.3s;
  border-top-color: #4ADE80;
}

.success-checkmark {
  width: 100%;
  height: 100%;
  animation: checkmarkDraw 0.6s ease-out 0.4s forwards;
  opacity: 0;
}

.checkmark-circle {
  stroke: #22C55E;
  stroke-width: 2;
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  animation: circleDraw 0.4s ease-out forwards;
}

.checkmark-path {
  stroke: #22C55E;
  stroke-width: 3;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: pathDraw 0.4s ease-out 0.3s forwards;
}

@keyframes successRing {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(1.5); opacity: 0; }
}

@keyframes circleDraw {
  to { stroke-dashoffset: 0; }
}

@keyframes pathDraw {
  to { stroke-dashoffset: 0; }
}

@keyframes checkmarkDraw {
  to { opacity: 1; transform: scale(1); }
}

/* Error Styles */
.status-container.error {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.04));
  border-color: #EF4444;
}

.error-animation {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 50%;
  animation: errorPulse 2s ease-in-out infinite;
}

.error-icon {
  width: 32px;
  height: 32px;
  color: #EF4444;
  stroke-width: 2.5;
}

@keyframes errorPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.3); }
  50% { box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }
}

.status-subtext {
  margin: 0;
  font-size: 13px;
  color: #888;
  font-weight: 400;
}

.error-message {
  color: #EF4444;
  font-weight: 500;
  background: rgba(239, 68, 68, 0.1);
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  max-width: 360px;
  word-break: break-word;
}

/* Buttons */
.status-button {
  padding: 12px 28px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  color: #fff;
  transition: all 0.2s ease;
  margin-top: 4px;
}

.status-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.status-button:active {
  transform: translateY(0) scale(0.98);
}

.success-button {
  background: linear-gradient(135deg, #22C55E, #16A34A);
}

.success-button:hover {
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.4);
}

.error-button {
  background: linear-gradient(135deg, #EF4444, #DC2626);
}

.error-button:hover {
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
}
</style>