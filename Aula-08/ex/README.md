# Documentação do FAQ - DevStack Solutions

Esta é a documentação técnica do portal de **Perguntas Frequentes (FAQ)** desenvolvido para a **DevStack Solutions**. O projeto foi estruturado seguindo as melhores práticas de desenvolvimento web moderno com foco em **escalabilidade**, **desempenho**, **acessibilidade (a11y)** e **responsividade**.

---

## 🛠️ Tecnologias Utilizadas

1. **HTML5 Semântico**: Estruturação clara para indexação (SEO) e tecnologias assistivas.
2. **CSS3 Modular**: Sistema de design moderno baseado em variáveis (Custom Properties) e transições suaves.
3. **Vanilla JavaScript (ES6+)**: Controle de eventos dinâmico e filtro de pesquisa instantâneo sem frameworks externos.

---

## 📁 Estrutura de Arquivos

```text
Aula-08/ex/
│
├── index.html   # Estrutura principal e conteúdo das perguntas
├── style.css    # Variáveis, layout flexível, animações e media queries
├── script.js    # Lógica de abertura do accordion e filtro em tempo real
└── README.md    # Esta documentação do projeto
```

---

## 💡 Recursos de Engenharia e Boas Práticas

### 1. Potencial de Escalabilidade
* **Filtro de Pesquisa Inteligente**: O mecanismo de busca normaliza os textos digitados (removendo letras maiúsculas, espaços extras e acentuações como `ã, é, ç`). Isso permite a busca precisa mesmo que o usuário digite com grafia diferente.
* **Atributo `data-question`**: Cada `.faq-item` possui um atributo customizado contendo palavras-chave invisíveis que auxiliam a busca. Se mais perguntas forem inseridas, o script as indexa automaticamente sem necessidade de qualquer alteração no código JS.

### 2. Acessibilidade (ARIA Attributes)
* Os botões que disparam a abertura das respostas possuem a propriedade `aria-expanded="false"` (mudando dinamicamente para `true`), permitindo que leitores de tela entendam o estado de expansão.
* Os contêineres de resposta utilizam `role="region"` associados ao ID de seu respectivo botão por meio de `aria-labelledby`.

### 3. Visual Limpo e Premium (Design System)
* **Contraste no Rodapé**: Conforme solicitado, o rodapé possui um tom escuro de alta visibilidade (`#0f172a`) contrastando fortemente com o fundo suave da página (`#f8fafc`).
* **Micro-interações**: Efeito Hover com elevação de card (`translateY(-2px)`), mudança sutil de borda para a cor principal da marca (índigo) e rotação suave do ícone indicador (`+` vira `x`).

### 4. Responsividade e Mobile First (Media Queries)
* O layout adapta-se de forma fluida a qualquer tamanho de viewport.
* Em celulares (telas menores que `768px` e `480px`):
  * O tamanho das fontes diminui proporcionalmente.
  * O cabeçalho se ajusta de horizontal para empilhamento vertical centralizado.
  * Tabelas internas contidas nas respostas ganham barra de rolagem horizontal automática para não quebrar a largura do dispositivo.

---

## 🚀 Como Executar o Projeto

1. Certifique-se de que os arquivos `index.html`, `style.css` e `script.js` estão na mesma pasta (`Aula-08/ex/`).
2. Dê um duplo clique no arquivo `index.html` ou use uma extensão de servidor local (ex: *Live Server* no VS Code) para abrir no navegador de sua preferência.
