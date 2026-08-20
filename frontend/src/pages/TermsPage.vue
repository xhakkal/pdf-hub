<template>
  <div class="w-full bg-brand min-h-screen flex flex-col antialiased">
    <!-- Main Content -->
    <main class="flex-grow max-w-3xl w-full mx-auto px-4 md:px-8 pt-[120px] pb-20 flex flex-col gap-8">
      <!-- Header -->
      <section class="text-center flex flex-col gap-3">
        <h1 class="text-5xl font-bold text-white">Termos de Uso</h1>
        <p class="text-lg text-muted">
          Leia nossos termos e condições antes de usar o PDFhub
        </p>
      </section>

      <!-- Content -->
      <div class="prose max-w-none">
        <!-- Section 1 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">1. Aceitação dos Termos</h2>
          <p class="text-muted">
            Ao acessar e utilizar o PDFhub, você concorda em cumprir com estes termos de uso. Se você não concordar com qualquer parte desses termos, por favor não utilize o serviço.
          </p>
        </div>

        <!-- Section 2 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">2. Uso Permitido</h2>
          <p class="text-muted">
            Você concorda em usar o PDFhub apenas para fins legais e de forma que não infrinja os direitos de terceiros ou restrinja o uso e aproveitamento do serviço por terceiros.
          </p>
          <ul class="list-disc list-inside space-y-2 text-muted">
            <li>Você não pode enviar malware ou conteúdo prejudicial</li>
            <li>Você não pode usar para fins comerciais sem permissão</li>
            <li>Você não pode tentar contornar as limitações de segurança</li>
          </ul>
        </div>

        <!-- Section 3 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">3. Limitação de Responsabilidade</h2>
          <p class="text-muted">
            O PDFhub é fornecido "como está" sem garantias de qualquer tipo. Não garantimos que o serviço será ininterrupto ou livre de erros.
          </p>
        </div>

        <!-- Section 4 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">4. Modificações dos Termos</h2>
          <p class="text-muted">
            Reservamo-nos o direito de modificar estes termos a qualquer momento. Suas alterações entrarão em vigor imediatamente após serem publicadas no site.
          </p>
        </div>

        <!-- Section 5 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">5. Contato</h2>
          <p class="text-muted">
            Se tiver dúvidas sobre estes termos, entre em contato conosco através do nosso formulário de suporte.
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'TermsPage'
}
</script>

<style scoped>
.prose {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>