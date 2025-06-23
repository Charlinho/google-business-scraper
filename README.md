# Google Business Scraper with Scrapy

🕷️ **Ferramenta profissional para capturar dados de empresas no Google usando Scrapy**

## 📋 Descrição

Este projeto utiliza **Scrapy**, o framework mais robusto para web scraping em Python, para extrair informações de empresas dos resultados de busca do Google. A solução é otimizada para:

- ✅ **Escalabilidade**: Processa milhares de resultados
- ✅ **Robustez**: Múltiplos seletores e tratamento de erros
- ✅ **Performance**: Requisições assíncronas e otimizadas
- ✅ **Anti-detecção**: Rotação de User-Agents e delays inteligentes

## 🆚 Scrapy vs Selenium

| Aspecto | Scrapy | Selenium |
|---------|--------|----------|
| **Performance** | ⚡ Muito rápido (assíncrono) | 🐌 Mais lento (browser real) |
| **Recursos** | 💾 Baixo consumo | 🔥 Alto consumo (RAM/CPU) |
| **Escalabilidade** | 📈 Excelente | 📉 Limitada |
| **JavaScript** | ❌ Não executa JS | ✅ Executa JS |
| **Complexidade** | 🎓 Curva de aprendizado | 🎯 Mais intuitivo |

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/google-business-scraper-scrapy.git
cd google-business-scraper-scrapy