/**
 * Arquivo: script.js
 * Descrição: Gerencia a transição de telas e exibição de dados do formulário de contato.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // Mapeamento dos elementos do DOM (Document Object Model)
    // ----------------------------------------------------
    
    // Contêineres de visualização (Views)
    const formView = document.getElementById('form-view');          // Tela inicial com os campos do formulário
    const confirmView = document.getElementById('confirm-view');    // Tela de confirmação dos dados
    const successView = document.getElementById('success-view');    // Tela de confirmação final (sucesso)

    // Elementos de cabeçalho do formulário
    const mainTitle = document.getElementById('main-title');        // Título principal do cartão
    const mainSubtitle = document.getElementById('main-subtitle');  // Subtítulo descritivo do cartão

    // Elementos de entrada (Inputs) do formulário
    const nomeInput = document.getElementById('nome');              // Campo para o nome do usuário
    const emailInput = document.getElementById('email');            // Campo para o e-mail do usuário
    const mensagemInput = document.getElementById('mensagem');      // Campo para a mensagem digitada

    // Elementos de exibição da tela de confirmação (onde os dados digitados serão mostrados)
    const confirmNome = document.getElementById('confirm-nome');    // Exibição do nome confirmado
    const confirmEmail = document.getElementById('confirm-email');  // Exibição do e-mail confirmado
    const confirmMensagem = document.getElementById('confirm-mensagem'); // Exibição da mensagem confirmada

    // Elementos de interação (Botões)
    const btnConfirmOk = document.getElementById('btn-confirm-ok');      // Botão que finaliza o envio dos dados
    const btnConfirmBack = document.getElementById('btn-confirm-back');  // Botão que retorna ao formulário para edição
    const btnSuccessReset = document.getElementById('btn-success-reset'); // Botão que permite enviar uma nova mensagem

    // ----------------------------------------------------
    // Eventos e Regras de Negócio
    // ----------------------------------------------------

    /**
     * Evento 1: Submissão do Formulário
     * Captura os dados inseridos, valida-os (via HTML5 required/email) e exibe na tela de confirmação.
     */
    formView.addEventListener('submit', (e) => {
        // Impede o comportamento padrão de recarregar a página (comum no envio de formulários)
        e.preventDefault();

        // Transfere os valores digitados nos inputs para os campos de texto da tela de confirmação
        confirmNome.textContent = nomeInput.value;
        confirmEmail.textContent = emailInput.value;
        confirmMensagem.textContent = mensagemInput.value;

        // Altera o título e o subtítulo da página de forma dinâmica
        mainTitle.textContent = 'Confirme seus Dados';
        mainSubtitle.textContent = 'Verifique se as informações abaixo estão corretas antes de enviar.';

        // Oculta a tela do formulário e mostra a tela de confirmação de dados
        formView.classList.add('view-hidden');
        confirmView.classList.remove('view-hidden');
    });

    /**
     * Evento 2: Retomar/Voltar para o Formulário
     * Permite que o usuário volte para editar os dados que ele já digitou sem perdê-los.
     */
    btnConfirmBack.addEventListener('click', () => {
        // Restaura o cabeçalho original da tela de contato
        mainTitle.textContent = 'Fale Conosco';
        mainSubtitle.textContent = 'Envie sua mensagem e entraremos em contato em breve.';

        // Oculta a tela de confirmação e exibe o formulário novamente
        confirmView.classList.add('view-hidden');
        formView.classList.remove('view-hidden');
    });

    /**
     * Evento 3: Confirmar Dados e Finalizar Envio
     * Exibe a tela final informando que o formulário foi enviado com sucesso.
     */
    btnConfirmOk.addEventListener('click', () => {
        // Ajusta os cabeçalhos para o estado final de sucesso
        mainTitle.textContent = 'Enviado!';
        mainSubtitle.textContent = '';

        // Oculta a tela de confirmação e mostra a tela de sucesso
        confirmView.classList.add('view-hidden');
        successView.classList.remove('view-hidden');
    });

    /**
     * Evento 4: Voltar para enviar um Novo Formulário
     * Reseta os campos do formulário original e o exibe novamente para um novo envio.
     */
    btnSuccessReset.addEventListener('click', () => {
        // Reseta todos os campos de texto do formulário original de uma só vez
        formView.reset();

        // Restaura o cabeçalho da página para o padrão inicial
        mainTitle.textContent = 'Fale Conosco';
        mainSubtitle.textContent = 'Envie sua mensagem e entraremos em contato em breve.';

        // Oculta a tela de sucesso e exibe o formulário vazio novamente
        successView.classList.add('view-hidden');
        formView.classList.remove('view-hidden');
    });
});
