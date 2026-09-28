#!/usr/bin/env python3
"""Gera as páginas de casos de uso a partir dos textos abaixo.

Uso:
    python3 scripts/gerar_casos.py

Reaproveita o <head>, o cabeçalho e o rodapé de index.html (PT) e en/index.html (EN),
então rode de novo sempre que mudar o menu ou o rodapé da página inicial.
Também atualiza as chamadas dos casos na página inicial, o sitemap.xml e o llms.txt.
"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ICONES = '''
    <symbol id="i-cal" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M8 3v4M16 3v4M3 10h18M8 14h2M14 14h2M8 17h2"/></symbol>
    <symbol id="i-doc" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M6 3h8l4 4v14H6z"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M14 3v4h4M9 12h6M9 16h6"/></symbol>
    <symbol id="i-folders" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3 7h6l2 2h10v10H3z"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M7 13h10M7 16h6"/></symbol>
    <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M16 16l4 4"/></symbol>'''

NOTA_PT = 'Cenário hipotético, criado para ilustrar como a plataforma funciona. Resultados dependem de cada operação e são medidos no piloto.'
NOTA_EN = 'Hypothetical scenario, created to show how the platform works. Results depend on each operation and are measured during the pilot.'

CASOS = [
    {
        'pt_slug': 'erp-medico-agenda-prontuario',
        'en_slug': 'medical-software-scheduling-records',
        'pt': dict(
            titulo='Agentes de IA para um ERP médico: agenda e prontuário em centenas de clínicas',
            desc='Caso de uso hipotético: uma empresa de software médico, que fornece chat e prontuário eletrônico para centenas de clínicas, incorpora ao seu sistema agentes de IA para agendamento e leitura de prontuário, com dados isolados por clínica e LGPD.',
            tag='Caso de uso · Saúde',
            h1='Agentes de IA dentro de um ERP médico: <span class="grad">agenda e prontuário para centenas de clínicas.</span>',
            chamada='Uma empresa de software médico, que fornece chat e prontuário eletrônico para centenas de clínicas, incorpora ao seu sistema um agente de agendamento e um agente que resume o prontuário, com a marca dela.',
            lead='Uma empresa de software médico fornece sistema de gestão, chat com pacientes e prontuário eletrônico para centenas de clínicas. Os clientes pedem IA: querem que o chat marque consultas sozinho e que o médico receba um resumo do prontuário antes de atender. Fazer isso internamente exigiria uma equipe de IA, uma infraestrutura segura para dados de saúde e um custo por clínica que coubesse no preço do sistema.',
            dores=[('Clientes pedindo IA', 'As clínicas querem agendamento automático e resumo de prontuário, e os concorrentes já anunciam recursos de IA.'),
                   ('Escala com isolamento', 'São centenas de clínicas, cada uma com suas regras, agendas e pacientes. Os dados de uma nunca podem aparecer para outra.'),
                   ('Custo e risco', 'Uma IA genérica cobrada por uso pode comer a margem do produto, e um erro com dado de saúde vira problema jurídico e de reputação.')],
            solucao='A solução: agentes dentro do produto, com a marca do ERP',
            agentes=[('i-cal', 'violet', 'Agente de agendamento no chat', 'Funciona dentro do chat que o ERP já oferece às clínicas, inclusive no WhatsApp. Marca, remarca, confirma e envia lembretes na agenda do próprio sistema, seguindo as regras de cada clínica. O que foge do padrão vai para a recepção, com a conversa inteira.'),
                     ('i-doc', 'teal', 'Agente de leitura de prontuário', 'Dentro do prontuário eletrônico, entrega ao profissional um resumo do histórico antes da consulta, com a fonte de cada informação: documento e data. Não faz diagnóstico nem prescrição; a decisão é sempre do profissional.'),
                     ('i-chip', 'orange', 'Integração com o ERP', 'A Cuboit conecta os agentes à agenda, ao chat e ao prontuário do sistema por API. As clínicas usam os recursos como parte do software que já conhecem, com a marca da empresa.')],
            jornada_t='A jornada de um paciente em uma das clínicas',
            jornada=[('i-chat', 'blue', 'Paciente', 'Pede um horário às 22h pelo WhatsApp da clínica, atendido pelo chat do ERP.'),
                     ('i-cal', 'violet', 'Agente de agendamento', 'Consulta a agenda no próprio sistema, marca a consulta e envia lembrete na véspera.'),
                     ('i-hand', 'orange', 'Recepção da clínica', 'Recebe só as exceções, como um encaixe urgente.'),
                     ('i-doc', 'teal', 'Agente de prontuário', 'Ao abrir o atendimento, o médico vê um resumo do histórico com as fontes.'),
                     ('i-user', 'pink', 'Médico', 'Confere as fontes, atende e decide. Cada acesso fica registrado.')],
            cuidados_t='Privacidade, segurança e controle',
            cuidados=['Cada clínica é um ambiente isolado: os dados nunca se misturam entre clientes do ERP', 'Acesso ao prontuário só com perfil autorizado, e cada leitura registrada',
                      'Dados de saúde tratados como dados sensíveis, conforme a LGPD', 'Resumo sempre com fonte, para o profissional conferir no original',
                      'Painel com uso e custo por clínica, para o ERP definir preço e margem', 'Recursos ligados clínica a clínica, como módulo adicional do sistema'],
            valor_t='Por que funciona para a empresa de software médico',
            valor='Ela lança recursos de IA no próprio produto sem montar uma equipe de IA e pode vendê-los como módulo adicional para toda a base de clínicas. A Cuboit implanta, opera e mantém os agentes; a empresa acompanha uso e custo de cada clínica num painel e controla a margem.',
            etapas=[('Diagnóstico', 'APIs do ERP, regras de agenda e estrutura do prontuário.', '2 a 3 semanas'),
                    ('Piloto com algumas clínicas', 'Agendamento no chat e resumo de prontuário para um grupo de clínicas clientes.', '4 a 6 semanas'),
                    ('Liberação para a base', 'O módulo é oferecido às demais clínicas e ligado clínica a clínica.', 'contínuo')],
        ),
        'en': dict(
            titulo='AI agents for medical software: scheduling and records across hundreds of clinics',
            desc='Hypothetical use case: a medical software company that provides chat and electronic health records to hundreds of clinics builds AI agents for scheduling and record summaries into its product, with each clinic’s data isolated.',
            tag='Use case · Healthcare',
            h1='AI agents inside medical practice software: <span class="grad">scheduling and records for hundreds of clinics.</span>',
            chamada='A medical software company that provides chat and electronic health records to hundreds of clinics builds a scheduling agent and a record summary agent into its product, under its own brand.',
            lead='A medical software company provides practice management, patient chat and electronic health records to hundreds of clinics. Its customers are asking for AI: they want the chat to book appointments on its own and doctors to get a record summary before each visit. Building that in-house would take an AI team, secure infrastructure for health data and a per-clinic cost that fits the product’s price.',
            dores=[('Customers asking for AI', 'Clinics want automatic scheduling and record summaries, and competitors already advertise AI features.'),
                   ('Scale with isolation', 'Hundreds of clinics, each with its own rules, calendars and patients. One clinic’s data can never show up for another.'),
                   ('Cost and risk', 'Generic pay-per-use AI can eat the product’s margin, and a mistake with health data becomes a legal and reputational problem.')],
            solucao='The solution: agents inside the product, under the software’s brand',
            agentes=[('i-cal', 'violet', 'Scheduling agent in the chat', 'Runs inside the chat the software already offers clinics, including WhatsApp. Books, reschedules, confirms and sends reminders in the system’s own calendar, following each clinic’s rules. Unusual requests go to the front desk with the full conversation.'),
                     ('i-doc', 'teal', 'Record summary agent', 'Inside the electronic health record, gives the professional a summary of the history before the visit, citing the source of every item: document and date. It does not diagnose or prescribe; the decision always stays with the professional.'),
                     ('i-chip', 'orange', 'Integration with the software', 'Cuboit connects the agents to the software’s calendar, chat and records through its API. Clinics use the features as part of the software they already know, under the company’s brand.')],
            jornada_t='One patient’s journey at one of the clinics',
            jornada=[('i-chat', 'blue', 'Patient', 'Asks for an appointment at 10 pm on the clinic’s WhatsApp, handled by the software’s chat.'),
                     ('i-cal', 'violet', 'Scheduling agent', 'Checks the calendar in the system itself, books the visit and sends a reminder the day before.'),
                     ('i-hand', 'orange', 'Clinic front desk', 'Only gets the exceptions, such as an urgent same-day slot.'),
                     ('i-doc', 'teal', 'Record summary agent', 'When the visit opens, the doctor sees a summary of the history with sources.'),
                     ('i-user', 'pink', 'Doctor', 'Checks the sources, sees the patient and decides. Every access is logged.')],
            cuidados_t='Privacy, security and control',
            cuidados=['Each clinic is an isolated environment: data never mixes between the software’s customers', 'Record access only for authorized roles, with every read logged',
                      'Health data treated as sensitive data under Brazil’s LGPD', 'Summaries always cite the source, so professionals can check the original',
                      'Dashboard with usage and cost per clinic, so the company can set price and margin', 'Features switched on clinic by clinic, as an add-on module'],
            valor_t='Why it works for the medical software company',
            valor='It launches AI features in its own product without building an AI team and can sell them as an add-on to its entire clinic base. Cuboit deploys, runs and maintains the agents; the company tracks usage and cost per clinic on a dashboard and controls its margin.',
            etapas=[('Assessment', 'The software’s APIs, scheduling rules and health record structure.', '2–3 weeks'),
                    ('Pilot with a few clinics', 'Scheduling in the chat and record summaries for a group of client clinics.', '4–6 weeks'),
                    ('Roll-out to the base', 'The module is offered to the other clinics and switched on clinic by clinic.', 'ongoing')],
        ),
    },
    {
        'pt_slug': 'governo-documentacao',
        'en_slug': 'government-documents',
        'pt': dict(
            titulo='Agentes de IA para prefeituras e governos: documentação de todas as secretarias',
            desc='Caso de uso hipotético: uma prefeitura ou governo estadual organiza a documentação de todas as secretarias com agentes de IA, responde servidores e cidadãos com fonte e mantém trilha de auditoria para LAI e LGPD.',
            tag='Caso de uso · Setor público',
            h1='Agentes de IA para prefeituras e governos: <span class="grad">toda a documentação, em todas as secretarias.</span>',
            chamada='Uma prefeitura ou governo estadual organiza documentos de todas as secretarias num só lugar, com agentes que respondem servidores e cidadãos sempre citando a fonte e registrando cada decisão.',
            lead='Uma prefeitura ou um governo estadual tem documentos espalhados por várias secretarias, como saúde, educação, obras, fazenda e administração, em papel, pastas de rede e sistemas que não conversam entre si. Servidores perdem horas procurando leis, decretos, processos e pareceres, e o cidadão espera dias por respostas simples.',
            dores=[('Documentos espalhados', 'Cada secretaria guarda de um jeito, em sistemas e pastas diferentes. Achar a versão certa de um decreto ou processo depende de quem sabe onde está.'),
                   ('Respostas lentas e desencontradas', 'A mesma pergunta recebe respostas diferentes conforme quem atende, e pedidos passam de mesa em mesa até chegar à secretaria certa.'),
                   ('Cobrança por transparência', 'A Lei de Acesso à Informação e os órgãos de controle exigem prazo, registro e justificativa de cada decisão.')],
            solucao='A solução: três agentes, uma base única',
            agentes=[('i-folders', 'violet', 'Agente de organização documental', 'Classifica e indexa os documentos de todas as secretarias por tipo, assunto, data e órgão, aponta versões e duplicidades e deixa tudo pesquisável num só lugar, respeitando quem pode ver o quê.'),
                     ('i-search', 'teal', 'Agente de consulta para servidores', 'Responde perguntas com base em leis, decretos, portarias e processos, sempre citando o documento de origem, e prepara minutas que um servidor revisa e assina.'),
                     ('i-chat', 'blue', 'Agente de atendimento ao cidadão', 'Tira dúvidas no site e no WhatsApp sobre serviços, documentos necessários e andamento de protocolos, e encaminha cada pedido para a secretaria certa, com registro.')],
            jornada_t='A jornada de um pedido',
            jornada=[('i-chat', 'blue', 'Cidadão', 'Pergunta no WhatsApp o que precisa para tirar um alvará de obra.'),
                     ('i-user', 'violet', 'Agente de atendimento', 'Lista os documentos com base na legislação local e abre o protocolo.'),
                     ('i-flow', 'orange', 'Cubo Flow', 'O protocolo vira um cartão e vai direto para a Secretaria de Obras.'),
                     ('i-search', 'teal', 'Agente de consulta', 'Mostra ao servidor a legislação e processos parecidos, com fonte.'),
                     ('i-hand', 'pink', 'Servidor responsável', 'Analisa, decide e assina. O cidadão é avisado, e tudo fica registrado.')],
            cuidados_t='Transparência e segurança',
            cuidados=['Permissões por secretaria e por cargo', 'Cada consulta e decisão registrada, com trilha de auditoria exportável',
                      'Respostas rastreáveis, que apoiam os pedidos da Lei de Acesso à Informação', 'Dados pessoais de cidadãos tratados conforme a LGPD',
                      'Implantação em nuvem soberana ou no ambiente do próprio órgão', 'Decisões sempre de um servidor responsável; o agente só apoia'],
            valor_t='Por que funciona para prefeituras e governos',
            valor='A gestão passa a enxergar todas as secretarias num painel, os servidores deixam de procurar documento e passam a decidir, e o cidadão tem resposta a qualquer hora. A prestação de contas fica mais simples, porque cada passo já nasce registrado.',
            etapas=[('Diagnóstico', 'Inventário de documentos, sistemas e fluxos em cada secretaria.', '2 a 4 semanas'),
                    ('Piloto em uma secretaria', 'Organização documental, consulta para servidores e atendimento de um tipo de serviço.', '6 a 8 semanas'),
                    ('Expansão', 'As demais secretarias entram uma a uma, na mesma base.', 'por secretaria')],
        ),
        'en': dict(
            titulo='AI agents for city halls and governments: documents across every department',
            desc='Hypothetical use case: a city hall or state government organizes documents from every department with AI agents, answers staff and citizens with sources, and keeps an audit trail for transparency and data protection laws.',
            tag='Use case · Public sector',
            h1='AI agents for city halls and governments: <span class="grad">every document, across every department.</span>',
            chamada='A city hall or state government brings documents from every department into one place, with agents that answer staff and citizens, always citing the source and logging every decision.',
            lead='A city hall or state government keeps documents across many departments, such as health, education, public works, finance and administration, on paper, in shared folders and in systems that don’t talk to each other. Staff lose hours looking for laws, decrees, cases and opinions, and citizens wait days for simple answers.',
            dores=[('Scattered documents', 'Each department stores files its own way, in different systems and folders. Finding the right version of a decree or case depends on who knows where it is.'),
                   ('Slow, inconsistent answers', 'The same question gets different answers depending on who replies, and requests bounce between desks before reaching the right department.'),
                   ('Pressure for transparency', 'Brazil’s Access to Information Law and oversight bodies require deadlines, records and a justification for every decision.')],
            solucao='The solution: three agents, one foundation',
            agentes=[('i-folders', 'violet', 'Document organization agent', 'Classifies and indexes documents from every department by type, subject, date and office, flags versions and duplicates, and makes everything searchable in one place, respecting who can see what.'),
                     ('i-search', 'teal', 'Staff research agent', 'Answers questions based on laws, decrees, ordinances and cases, always citing the source document, and drafts documents that a civil servant reviews and signs.'),
                     ('i-chat', 'blue', 'Citizen service agent', 'Answers questions on the website and WhatsApp about services, required documents and case status, and routes every request to the right department, with a record.')],
            jornada_t='One request’s journey',
            jornada=[('i-chat', 'blue', 'Citizen', 'Asks on WhatsApp what is needed for a building permit.'),
                     ('i-user', 'violet', 'Service agent', 'Lists the documents based on local law and opens a case.'),
                     ('i-flow', 'orange', 'Cubo Flow', 'The case becomes a card and goes straight to the Public Works department.'),
                     ('i-search', 'teal', 'Research agent', 'Shows the civil servant the relevant law and similar cases, with sources.'),
                     ('i-hand', 'pink', 'Civil servant in charge', 'Reviews, decides and signs. The citizen is notified, and everything is logged.')],
            cuidados_t='Transparency and security',
            cuidados=['Permissions by department and role', 'Every query and decision logged, with an exportable audit trail',
                      'Traceable answers that support access-to-information requests', 'Citizens’ personal data handled under Brazil’s LGPD',
                      'Deployment on a sovereign cloud or in the agency’s own environment', 'Decisions always made by a responsible civil servant; the agent only assists'],
            valor_t='Why it works for city halls and governments',
            valor='Leadership sees every department on one dashboard, staff stop searching for documents and start deciding, and citizens get answers at any hour. Accountability gets simpler because every step is recorded from the start.',
            etapas=[('Assessment', 'Inventory of documents, systems and workflows in each department.', '2–4 weeks'),
                    ('Pilot in one department', 'Document organization, staff research and citizen service for one type of request.', '6–8 weeks'),
                    ('Expansion', 'The other departments join one by one, on the same foundation.', 'per department')],
        ),
    },
]

IDIOMAS = {
    'pt': dict(fonte='index.html', base='/casos/', home='/', voltar='← Todos os cases', voltar_href='/#cases',
               etapa='etapa', etapas_t='Como a Cuboit implanta', nota=NOTA_PT, lang_label='Idioma',
               cta_t='Tem uma operação parecida?', cta='Em 30 minutos avaliamos o seu caso e mostramos como ficaria na plataforma Cuboit.',
               cta_btn='Agendar diagnóstico', cta_href='/#contato', dores_t='O problema', lang='pt-BR'),
    'en': dict(fonte='en/index.html', base='/en/cases/', home='/en/', voltar='← All cases', voltar_href='/en/#cases',
               etapa='step', etapas_t='How Cuboit rolls it out', nota=NOTA_EN, lang_label='Language',
               cta_t='Running a similar operation?', cta='In 30 minutes we assess your case and show what it would look like on the Cuboit platform.',
               cta_btn='Book an assessment', cta_href='/en/#contact', dores_t='The problem', lang='en'),
}


def url(caso, idioma):
    return 'https://cuboit.com.br' + IDIOMAS[idioma]['base'] + caso[idioma + '_slug'] + '/'


def sem_tags(html):
    return re.sub('<[^>]+>', '', html)


def pagina(caso, idioma):
    I, T = IDIOMAS[idioma], caso[idioma]
    src = open(os.path.join(RAIZ, I['fonte']), encoding='utf-8').read()
    head = src[:src.index('<body>')]
    sprite = src[src.index('<svg width="0"'):src.index('<header class="nav">')]
    header = src[src.index('<header class="nav">'):src.index('</header>') + len('</header>')]
    footer = src[src.index('<footer>'):src.index('</footer>') + len('</footer>')]
    script = re.search(r'<script src="[^"]*js/main\.js[^"]*"></script>', src).group(0)
    u_pt, u_en, u = url(caso, 'pt'), url(caso, 'en'), url(caso, idioma)

    # <head>: textos, endereços e dados estruturados próprios do caso
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head, flags=re.S)
    titulo = T['titulo'] + ' — Cuboit'
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titulo, head)
    for nome in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        head = re.sub(r'(<meta %s content=")[^"]*"' % nome, r'\g<1>%s"' % T['desc'].replace('\\', ''), head)
    for nome in ['property="og:title"', 'name="twitter:title"']:
        head = re.sub(r'(<meta %s content=")[^"]*"' % nome, r'\g<1>%s"' % titulo, head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % u, head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*"', r'\g<1>%s"' % u, head)
    head = head.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    head = re.sub(r'<link rel="alternate" hreflang="pt-BR" href="[^"]*">', '<link rel="alternate" hreflang="pt-BR" href="%s">' % u_pt, head)
    head = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*">', '<link rel="alternate" hreflang="en" href="%s">' % u_en, head)
    head = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="%s">' % u_pt, head)
    head = re.sub(r'(href|src)="(\.\./)?(images|css|js)/', r'\1="/\3/', head)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": sem_tags(T['h1']), "description": T['desc'], "inLanguage": I['lang'], "url": u,
         "datePublished": "2026-09-28",
         "author": {"@type": "Organization", "name": "Cuboit", "url": "https://cuboit.com.br/"},
         "publisher": {"@type": "Organization", "name": "Cuboit",
                       "logo": {"@type": "ImageObject", "url": "https://cuboit.com.br/images/logos/png/cuboit-simbolo-cor.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Cuboit", "item": "https://cuboit.com.br" + I['home']},
            {"@type": "ListItem", "position": 2, "name": "Cases", "item": "https://cuboit.com.br" + I['voltar_href']},
            {"@type": "ListItem", "position": 3, "name": sem_tags(T['h1']), "item": u}]}]}
    head = head.replace('</head>', '<script type="application/ld+json">\n%s\n</script>\n</head>' % json.dumps(ld, ensure_ascii=False, indent=1))

    # cabeçalho e rodapé: links apontam para as seções da página inicial
    casa = I['home']
    # só links <a>: o <use href="#..."> dos ícones precisa continuar local
    ancora_casa = lambda m: '%s href="%s#%s"' % (m.group(1), casa, m.group(2))
    header = re.sub(r'(<a\b[^>]*?) href="#([a-z-]+)"', ancora_casa, header)
    footer = re.sub(r'(<a\b[^>]*?) href="#([a-z-]+)"', ancora_casa, footer)
    for ancora in ('topo', 'top'):
        header = header.replace('href="%s#%s"' % (casa, ancora), 'href="%s"' % casa)
        footer = footer.replace('href="%s#%s"' % (casa, ancora), 'href="%s"' % casa)
    pt_path, en_path = u_pt.replace('https://cuboit.com.br', ''), u_en.replace('https://cuboit.com.br', '')
    lang_nav = '<nav class="lang" aria-label="%s"><a href="%s" hreflang="pt-BR"%s>PT</a><a href="%s" hreflang="en"%s>EN</a></nav>' % (
        I['lang_label'], pt_path, ' aria-current="page"' if idioma == 'pt' else ' lang="pt-BR"',
        en_path, ' aria-current="page"' if idioma == 'en' else ' lang="en"')
    header = re.sub(r'<nav class="lang".*?</nav>', lang_nav, header, flags=re.S)
    sprite = sprite.replace('  </defs>\n</svg>', ICONES + '\n  </defs>\n</svg>', 1)
    script = re.sub(r'src="(\.\./)?js/', 'src="/js/', script)

    dores = ''.join('<div class="pain"><b>%s</b><p>%s</p></div>' % d for d in T['dores'])
    agentes = ''.join('\n          <div><div class="tile t-%s"><svg><use href="#%s"/></svg></div><b>%s</b><p>%s</p></div>' % (c, i, t, x)
                      for i, c, t, x in T['agentes'])
    jornada = ''.join('\n          <li><div class="tile t-%s"><svg><use href="#%s"/></svg></div><div><b>%s</b><p>%s</p></div></li>' % (c, i, a, x)
                      for i, c, a, x in T['jornada'])
    cuidados = ''.join('<li>%s</li>' % c for c in T['cuidados'])
    etapas = ''.join('<div class="step"><span class="n">%s %d</span><h3>%s</h3><p>%s</p><span class="dur">%s</span></div>' % (I['etapa'], n + 1, a, b, c)
                     for n, (a, b, c) in enumerate(T['etapas']))

    main = f'''<main id="topo" class="case-page">

<section class="case-hero">
  <div class="wrap">
    <a class="case-back" href="{I['voltar_href']}">{I['voltar']}</a>
    <span class="uc-tag">{T['tag']}</span>
    <h1>{T['h1']}</h1>
    <p class="lead">{T['lead']}</p>
  </div>
</section>

<section class="case-sec">
  <div class="wrap">
    <h2 class="case-h2">{I['dores_t']}</h2>
    <div class="pains">{dores}</div>
  </div>
</section>

<section class="case-sec soft">
  <div class="wrap">
    <h2 class="case-h2">{T['solucao']}</h2>
    <div class="usecase">
      <div class="uc-main">
        <div class="uc-agents">{agentes}
        </div>
        <div class="uc-care"><b>{T['cuidados_t']}</b><ul>{cuidados}</ul></div>
      </div>
      <div class="uc-journey">
        <b>{T['jornada_t']}</b>
        <ol>{jornada}
        </ol>
      </div>
    </div>
  </div>
</section>

<section class="case-sec">
  <div class="wrap case-biz">
    <h2 class="case-h2">{T['valor_t']}</h2>
    <p class="lead">{T['valor']}</p>
  </div>
</section>

<section class="case-sec soft">
  <div class="wrap">
    <h2 class="case-h2">{I['etapas_t']}</h2>
    <div class="steps steps-3">{etapas}</div>
    <p class="case-note">{I['nota']}</p>
  </div>
</section>

<section class="case-sec">
  <div class="wrap">
    <div class="final case-cta">
      <div style="position:relative;z-index:1">
        <h2>{I['cta_t']}</h2>
        <p class="lead">{I['cta']}</p>
      </div>
      <div style="position:relative;z-index:1;align-self:center;justify-self:start"><a class="btn btn-light" href="{I['cta_href']}">{I['cta_btn']} <span aria-hidden="true">→</span></a></div>
    </div>
  </div>
</section>

</main>
'''
    return head + '<body>\n\n' + sprite + header + '\n\n' + main + '\n' + footer + '\n\n' + script + '\n</body>\n</html>\n'


CHAMADAS = {
    'pt': dict(arquivo='index.html', rotulo='Casos de uso · cenários ilustrativos', ler='Ler o caso'),
    'en': dict(arquivo='en/index.html', rotulo='Use cases · illustrative scenarios', ler='Read the case'),
}


def atualizar_home(idioma):
    """Reescreve as chamadas dos casos na seção Cases da página inicial."""
    C, I = CHAMADAS[idioma], IDIOMAS[idioma]
    caminho = os.path.join(RAIZ, C['arquivo'])
    s = open(caminho, encoding='utf-8').read()
    cards = ''.join('''
      <a class="case-feature" href="%s%s/">
        <div><span class="uc-tag">%s</span><h3>%s</h3><p>%s</p></div>
        <span class="go">%s <span aria-hidden="true">→</span></span>
      </a>''' % (I['base'], c[idioma + '_slug'], c[idioma]['tag'], c[idioma]['titulo'], c[idioma]['chamada'], C['ler']) for c in CASOS)
    bloco = '    <p class="eyebrow case-features-label">%s</p>\n    <div class="case-features">%s\n    </div>\n' % (C['rotulo'], cards)
    s, n = re.subn(r'    <p class="eyebrow case-features-label">.*?</p>\n    <div class="case-features">.*?\n    </div>\n', lambda m: bloco, s, flags=re.S)
    if n != 1:
        raise SystemExit('Não encontrei as chamadas dos casos em ' + C['arquivo'])
    open(caminho, 'w', encoding='utf-8').write(s)


def atualizar_sitemap():
    caminho = os.path.join(RAIZ, 'sitemap.xml')
    s = open(caminho, encoding='utf-8').read()
    s = re.sub(r'  <url>\n    <loc>https://cuboit\.com\.br/(casos|en/cases)/.*?</url>\n', '', s, flags=re.S)
    extra = ''
    for c in CASOS:
        u_pt, u_en = url(c, 'pt'), url(c, 'en')
        for loc in (u_pt, u_en):
            extra += ('  <url>\n    <loc>%s</loc>\n    <lastmod>2026-09-28</lastmod>\n'
                      '    <xhtml:link rel="alternate" hreflang="pt-BR" href="%s"/>\n'
                      '    <xhtml:link rel="alternate" hreflang="en" href="%s"/>\n  </url>\n') % (loc, u_pt, u_en)
    open(caminho, 'w', encoding='utf-8').write(s.replace('</urlset>', extra + '</urlset>'))


def atualizar_llms():
    caminho = os.path.join(RAIZ, 'llms.txt')
    s = open(caminho, encoding='utf-8').read()
    lista = ''.join('- [%s](%s): %s\n' % (c['pt']['titulo'], url(c, 'pt'), c['pt']['chamada']) for c in CASOS)
    s = re.sub(r'## Casos de uso.*?\n\n', lambda m: '## Casos de uso (hipotéticos)\n' + lista + '\n', s, flags=re.S)
    open(caminho, 'w', encoding='utf-8').write(s)


def main():
    import shutil
    for idioma in ('pt', 'en'):
        pasta = os.path.join(RAIZ, IDIOMAS[idioma]['base'].strip('/'))
        shutil.rmtree(pasta, ignore_errors=True)  # remove casos que saíram da lista
    for caso in CASOS:
        for idioma in ('pt', 'en'):
            destino = os.path.join(RAIZ, IDIOMAS[idioma]['base'].strip('/'), caso[idioma + '_slug'], 'index.html')
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with open(destino, 'w', encoding='utf-8') as f:
                f.write(pagina(caso, idioma))
            print('gerado', os.path.relpath(destino, RAIZ))
    for idioma in ('pt', 'en'):
        atualizar_home(idioma)
    atualizar_sitemap()
    atualizar_llms()
    print('página inicial, sitemap.xml e llms.txt atualizados')


if __name__ == '__main__':
    main()
