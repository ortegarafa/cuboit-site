<?php
/*
 * Cuboit — envio do formulário "Agendar diagnóstico" por e-mail.
 * Roda na hospedagem KingHost usando o envio de e-mail do próprio servidor (SMTP WEB).
 *
 * Regra da KingHost: o remetente (REMETENTE) precisa ser uma conta de e-mail
 * que exista e esteja ativa no domínio hospedado. A resposta vai para o visitante via Reply-To.
 */

// ===== Configuração =====
const DESTINO   = 'contato@cuboit.com.br';   // quem recebe os pedidos
const REMETENTE = 'contato@cuboit.com.br';   // conta existente no domínio (exigência da KingHost)
const ORIGENS   = ['https://cuboit.com.br', 'https://www.cuboit.com.br'];
// ========================

header('Content-Type: application/json; charset=utf-8');

function responder(int $status, array $dados): void {
    http_response_code($status);
    echo json_encode($dados, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    responder(405, ['ok' => false, 'erro' => 'metodo']);
}

// Aceita só envios vindos do próprio site
$origem = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origem !== '' && !in_array($origem, ORIGENS, true)) {
    responder(403, ['ok' => false, 'erro' => 'origem']);
}

// Campo isca: pessoas não veem, robôs preenchem. Finge sucesso para não dar pista.
if (!empty($_POST['website'])) {
    responder(200, ['ok' => true]);
}

// Remove quebras de linha para impedir injeção de cabeçalhos
function linha(string $campo, int $max): string {
    $v = trim((string)($_POST[$campo] ?? ''));
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);
    return mb_substr($v, 0, $max);
}

$nome      = linha('nome', 120);
$empresa   = linha('empresa', 120);
$email     = linha('email', 160);
$interesse = linha('interesse', 80);
$idioma    = linha('idioma', 10);
$pais      = linha('pais', 2);
$telefone  = linha('telefone', 40);
$tel164    = linha('telefone_e164', 20);
$mensagem  = mb_substr(trim((string)($_POST['msg'] ?? '')), 0, 3000);

if ($nome === '' || $empresa === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)
    || !preg_match('/^\+[1-9]\d{6,14}$/', $tel164)) {
    responder(422, ['ok' => false, 'erro' => 'campos']);
}

$assunto = 'Novo pedido de diagnóstico — ' . $empresa;
$corpo = "Novo pedido pelo site cuboit.com.br\n\n"
       . "Nome: $nome\n"
       . "Empresa: $empresa\n"
       . "E-mail: $email\n"
       . "Telefone: $telefone ($pais)\n"
       . "WhatsApp: https://wa.me/" . ltrim($tel164, '+') . "\n"
       . "Interesse: $interesse\n"
       . "Idioma da página: $idioma\n\n"
       . "Processo que quer automatizar:\n$mensagem\n\n"
       . "Enviado em " . date('d/m/Y H:i') . " · IP " . ($_SERVER['REMOTE_ADDR'] ?? '-') . "\n";

// Formato recomendado pela KingHost: cabeçalhos separados por \n, Return-Path do domínio e sem 5º parâmetro
$cabecalhos = implode("\n", [
    'From: Site Cuboit <' . REMETENTE . '>',
    'Reply-To: ' . $email,
    'Return-Path: ' . REMETENTE,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
]);

$assuntoCodificado = '=?UTF-8?B?' . base64_encode($assunto) . '?=';
$enviado = @mail(DESTINO, $assuntoCodificado, $corpo, $cabecalhos);
$tentativa = 'sem -f';
if (!$enviado) {
    $enviado = @mail(DESTINO, $assuntoCodificado, $corpo, $cabecalhos, '-f' . REMETENTE);
    $tentativa = 'com -f';
}

// Registro técnico de cada tentativa (sem dados pessoais), para diagnóstico
$erro = error_get_last();
@file_put_contents(__DIR__ . '/.envios.log', sprintf(
    "%s | %s | %s | %s\n",
    date('Y-m-d H:i:s'),
    $enviado ? 'OK' : 'FALHOU',
    $tentativa,
    $enviado ? '-' : ($erro['message'] ?? 'mail() retornou false')
), FILE_APPEND | LOCK_EX);

if (!$enviado) {
    responder(500, ['ok' => false, 'erro' => 'envio']);
}
responder(200, ['ok' => true]);
