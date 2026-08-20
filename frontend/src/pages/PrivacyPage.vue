<template>
  <div class="w-full bg-brand min-h-screen flex flex-col antialiased">
    <!-- Main Content -->
    <main class="flex-grow max-w-3xl w-full mx-auto px-4 md:px-8 pt-[120px] pb-20 flex flex-col gap-8">
      <!-- Header -->
      <section class="text-center flex flex-col gap-3">
        <h1 class="text-5xl font-bold text-white">Política de Privacidade</h1>
        <p class="text-lg text-muted">
          Saiba como o PDFhub coleta, usa e protege seus dados
        </p>
      </section>

      <!-- Content -->
      <div class="prose max-w-none">
        <!-- Section 1 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">1. Informações que Coletamos</h2>
          <p class="text-muted">
            Coletamos informações limitadas para operar nosso serviço:
          </p>
          <ul class="list-disc list-inside space-y-2 text-muted">
            <li>Arquivos que você carrega (processados temporariamente)</li>
            <li>Informações do navegador (cookies e identificadores de sessão)</li>
            <li>Endereço IP para fins de segurança e análise</li>
          </ul>
        </div>

        <!-- Section 2 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">2. Como Usamos Seus Dados</h2>
          <p class="text-muted">
            Seus dados são usados exclusivamente para:
          </p>
          <ul class="list-disc list-inside space-y-2 text-muted">
            <li>Processar suas conversões de arquivos</li>
            <li>Melhorar a qualidade do serviço</li>
            <li>Manter a segurança da plataforma</li>
            <li>Análise estatística anônima</li>
          </ul>
        </div>

        <!-- Section 3 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">3. Retenção de Dados</h2>
          <p class="text-muted">
            Os arquivos que você carrega são automaticamente deletados após 1 hora. Não armazenamos seus documentos permanentemente.
          </p>
        </div>

        <!-- Section 4 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">4. Compartilhamento de Dados</h2>
          <p class="text-muted">
            Nunca compartilhamos seus dados pessoais ou documentos com terceiros. Você tem total controle sobre seus arquivos.
          </p>
        </div>

        <!-- Section 5 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">5. Seus Direitos</h2>
          <p class="text-muted">
            Você tem o direito de solicitar acesso, correção ou exclusão de seus dados. Entre em contato conosco para exercer esses direitos.
          </p>
        </div>

        <!-- Section 6 -->
        <div class="bg-elevated rounded-xl p-6 border border-brand flex flex-col gap-4">
          <h2 class="text-2xl font-bold text-white">6. Contato</h2>
          <p class="text-muted">
            Para dúvidas sobre privacidade, entre em contato conosco através do nosso formulário de suporte.
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'PrivacyPage'
}
</script>

<style scoped>
.prose {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>