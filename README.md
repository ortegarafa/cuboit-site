# cuboit.com.br

Site institucional da Cuboit: agentes de IA para empresas.

Site estático (HTML, CSS e JS) hospedado na KingHost. O formulário é enviado pelo Formspree.

```
index.html      página em português
en/             página em inglês
css/  js/       estilos e scripts compartilhados
images/         logos e favicons
scripts/        publicar.py (envio por FTP a partir do seu computador)
.htaccess       HTTPS, redirecionamentos do site antigo, cache
robots.txt  sitemap.xml  llms.txt   buscadores e assistentes de IA
404.html        página de erro
```

Para ver localmente: `python3 -m http.server 8080` e abra http://localhost:8080.

Para publicar: siga o [PUBLICAR.md](PUBLICAR.md).
