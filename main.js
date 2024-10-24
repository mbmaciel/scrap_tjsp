const express = require('express');
const puppeteer = require('puppeteer');

const app = express();
const port = 3000;

// Define a rota principal
app.get('/scrape', async (req, res) => {
    try {
        const browser = await puppeteer.launch({
            headless: true, // Pode ser alterado para false se quiser visualizar o navegador
            args: ['--no-sandbox', '--disable-setuid-sandbox'] // Necessário em alguns ambientes, como servidores de hospedagem
        });
        const page = await browser.newPage();
        const timeout = 5000;
        page.setDefaultTimeout(timeout);

        // Configura o viewport
        await page.setViewport({
            width: 1405,
            height: 923
        });

        // Acessa a página inicial do processo
        await page.goto('https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NMPARTE&dadosConsulta.valorConsulta=Banco+Itau&cdForo=71');

        // Espera pelo primeiro link de processo e clica nele
        await Promise.all([
            page.waitForNavigation(),
            page.click('#listagemDeProcessos > ul:nth-of-type(1) a')
        ]);

        // Clica no link de movimentações
        await page.click('#linkmovimentacoes');

        // Aguarda o carregamento das movimentações e extrai o conteúdo
        const movimentacoes = await page.evaluate(() => {
            const element = document.querySelector('#tabelaTodasMovimentacoes'); // Supondo que as movimentações estão numa tabela com este ID
            return element ? element.innerText : 'Movimentações não encontradas';
        });

        await browser.close();

        // Retorna as movimentações como resposta JSON
        res.json({ movimentacoes });

    } catch (err) {
        console.error('Erro durante a automação:', err);
        res.status(500).json({ error: 'Erro ao buscar movimentações' });
    }
});

// Inicia o servidor
app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
