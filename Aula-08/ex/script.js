/**
 * DevStack Solutions - FAQ Script
 * Interatividade da sanfona (accordion) e filtro de pesquisa em tempo real.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ----------------------------------------------------
    // 1. Funcionalidade de Sanfona (Accordion)
    // ----------------------------------------------------
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const trigger = item.querySelector('.faq-trigger');
        const content = item.querySelector('.faq-content');

        trigger.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Fecha outros itens abertos para manter uma interface limpa e organizada (opcional, melhora a UX)
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                    const otherTrigger = otherItem.querySelector('.faq-trigger');
                    const otherContent = otherItem.querySelector('.faq-content');
                    otherTrigger.setAttribute('aria-expanded', 'false');
                    otherContent.style.maxHeight = null;
                }
            });

            // Alterna o estado do item atual
            if (isActive) {
                item.classList.remove('active');
                trigger.setAttribute('aria-expanded', 'false');
                content.style.maxHeight = null;
            } else {
                item.classList.add('active');
                trigger.setAttribute('aria-expanded', 'true');
                // Define a altura máxima dinamicamente baseado no conteúdo interno
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });

    // ----------------------------------------------------
    // 2. Sistema de Busca e Filtro com Tratamento de Acentos
    // ----------------------------------------------------
    const searchInput = document.getElementById('search-input');
    const noResultsMessage = document.getElementById('no-results');

    /**
     * Auxiliar para normalizar o texto removendo acentos e convertendo para minúsculas
     */
    function normalizeText(text) {
        return text
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, ''); // Remove acentos
    }

    searchInput.addEventListener('input', (e) => {
        const searchTerm = normalizeText(e.target.value.trim());
        let visibleCount = 0;

        faqItems.forEach(item => {
            const questionText = normalizeText(item.querySelector('.faq-question').textContent);
            const answerText = normalizeText(item.querySelector('.faq-answer').textContent);
            const dataQuestion = normalizeText(item.getAttribute('data-question') || '');

            // Verifica se o termo de pesquisa está na pergunta, resposta ou metadados de busca
            const isMatch = questionText.includes(searchTerm) || 
                            answerText.includes(searchTerm) || 
                            dataQuestion.includes(searchTerm);

            if (isMatch) {
                item.style.display = 'block';
                visibleCount++;
            } else {
                item.style.display = 'none';
                
                // Se o item que foi ocultado estava aberto, fechamos ele
                if (item.classList.contains('active')) {
                    item.classList.remove('active');
                    const trigger = item.querySelector('.faq-trigger');
                    const content = item.querySelector('.faq-content');
                    trigger.setAttribute('aria-expanded', 'false');
                    content.style.maxHeight = null;
                }
            }
        });

        // Mostra ou oculta mensagem de feedback caso nada seja encontrado
        if (visibleCount === 0) {
            noResultsMessage.classList.remove('hidden');
        } else {
            noResultsMessage.classList.add('hidden');
        }
    });

    // Redimensionamento de janela dinâmico (ajusta a altura máxima de itens abertos se a largura mudar)
    window.addEventListener('resize', () => {
        faqItems.forEach(item => {
            if (item.classList.contains('active')) {
                const content = item.querySelector('.faq-content');
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });
});
