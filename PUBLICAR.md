# Publicar o site novo na KingHost

Roteiro para trocar o WordPress antigo pelo site novo em cuboit.com.br.

## Situação atual (levantada em 28/09/2026)

- WordPress 5.1 (2019), tema `wp`, desatualizado. Painel público em `/wp-login.php`.
- Páginas: `/home/`, `/institucional/`, `/servicos/` (+4 subpáginas), `/cases/`, `/contato/`, `/noticias/`.
- Posts: 2 notícias antigas e 3 cases (Cremeb, Despachante Móvel, Vistorias Online).
- Sem sitemap. `www` já redireciona para sem `www`.
- **E-mail e DNS ficam na KingHost** (MX `mx-vip-01/02.kinghost.net`). Trocar os arquivos do site **não mexe no e-mail**. Não altere DNS nem MX.

## 1. Antes de tudo: backup

1. No painel da KingHost, faça backup do banco de dados do WordPress (phpMyAdmin → Exportar → SQL). Guarde o arquivo fora do servidor.
2. Por FTP, baixe a pasta pública inteira do site (normalmente `www/` ou `public_html/`) para o seu computador.

## 2. Preparar

1. Confirme que a conta `contato@cuboit.com.br` existe e está ativa no painel de e-mails. Se o endereço for outro, ajuste `DESTINO` e `REMETENTE` no `enviar.php`.
2. Confirme que o plano tem PHP ativo (planos Linux têm).
3. Confirme que o certificado SSL (HTTPS) está ativo para `cuboit.com.br` e `www.cuboit.com.br`.

## 3. Trocar os arquivos

### Opção A — pelo GitHub (recomendado)

1. No GitHub, em **Settings → Secrets and variables → Actions → New repository secret**, cadastre:
   - `FTP_SERVER`: host de FTP (painel KingHost → Gerenciar FTP)
   - `FTP_USERNAME`: usuário de FTP
   - `FTP_PASSWORD`: senha de FTP
   - `FTP_SERVER_DIR` (opcional): pasta pública com barra no fim. Não é necessário: o FTP da KingHost já abre em `/www`
2. Faça o backup (passo 1) e mova o WordPress para fora da pasta pública (item 1 da opção B).
3. Na aba **Actions → Publicar na KingHost → Run workflow**:
   - primeiro com **"Só simular" marcado**: confira no registro a lista do que seria enviado e a pasta de destino;
   - depois com **"Só simular" desmarcado**, para enviar de verdade.
4. Se der erro de conexão com `ftps`, rode de novo escolhendo `ftp`.

### Opção B — manual, por FTP

1. Por FTP, crie a pasta `_wordpress_antigo` **fora** da pasta pública (um nível acima) e mova para ela todo o conteúdo atual da pasta pública.
   - Se o FTP não permitir sair da pasta pública, baixe tudo (passo 1.2) e depois apague da pasta pública.
2. Envie para a pasta pública **somente** estes itens:

```
.htaccess
index.html
404.html
enviar.php
robots.txt
sitemap.xml
llms.txt
en/
css/
js/
images/
```

**Não envie:** `proposta-comunicacao.html` (confidencial), `PUBLICAR.md`, `.claude/`, `.DS_Store`.

> O `.htaccess` fica oculto em alguns programas de FTP. No FileZilla: menu Servidor → Forçar exibição de arquivos ocultos.

## 4. Testar (logo após subir)

- [ ] `https://cuboit.com.br` abre o site novo
- [ ] `http://cuboit.com.br` e `https://www.cuboit.com.br` redirecionam para `https://cuboit.com.br`
- [ ] `https://cuboit.com.br/en/` abre a versão em inglês
- [ ] Botões PT/EN e modo claro/escuro funcionam
- [ ] Endereços antigos redirecionam: `/contato/` → contato, `/servicos/` → consultoria, `/cases/` → cases
- [ ] `/wp-login.php` e `/noticias/` respondem "página removida" (410)
- [ ] Um endereço inventado (ex.: `/teste123`) mostra a página 404 da Cuboit
- [ ] Formulário: enviar um pedido de teste e conferir se o e-mail chegou (olhe também o spam)
- [ ] Testar no celular

Se algo der muito errado: apague os arquivos novos e mova de volta o conteúdo de `_wordpress_antigo`.

## 5. Buscadores e IAs (primeira semana)

1. **Google Search Console** (search.google.com/search-console): adicione `cuboit.com.br`, valide pelo DNS na KingHost e envie `https://cuboit.com.br/sitemap.xml`. Isso vale para a Busca e o Gemini.
2. **Bing Webmaster Tools** (bing.com/webmasters): dá para importar direto do Search Console. O Bing alimenta buscas de vários assistentes.
3. Peça a indexação da home e de `/en/` nas duas ferramentas.

## 6. Depois de 30 dias sem problemas

- Apague a pasta `_wordpress_antigo` do servidor e o banco de dados do WordPress (mantenha o backup do passo 1 guardado).
