#!/usr/bin/env python3
"""Envia o site da Cuboit para a KingHost por FTP (criptografado quando possível).

Uso:
    python3 scripts/publicar.py HOST USUARIO [PASTA_REMOTA]

A senha é pedida no terminal e não é salva. Nada é apagado no servidor:
arquivos com o mesmo nome são substituídos e o resto fica como está.
"""
import ftplib
import getpass
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Só o que deve ficar público
ARQUIVOS = [".htaccess", "index.html", "404.html", "enviar.php",
            "robots.txt", "sitemap.xml", "llms.txt"]
PASTAS = ["en", "css", "js", "images"]
IGNORAR = {".DS_Store"}


def conectar(host, usuario, senha):
    try:
        ftp = ftplib.FTP_TLS(host, timeout=30)
        ftp.login(usuario, senha)
        ftp.prot_p()
        print("Conectado com criptografia (FTPS).")
        return ftp
    except ftplib.error_perm:
        raise
    except Exception as erro:
        print(f"FTPS indisponível ({erro}); tentando FTP comum.")
        ftp = ftplib.FTP(host, timeout=30)
        ftp.login(usuario, senha)
        return ftp


def garantir_pasta(ftp, caminho):
    atual = ""
    for parte in caminho.split("/"):
        if not parte:
            continue
        atual = f"{atual}/{parte}" if atual else parte
        try:
            ftp.mkd(atual)
        except ftplib.error_perm:
            pass  # já existe


def enviar(ftp, local, remoto):
    with open(os.path.join(RAIZ, local), "rb") as f:
        ftp.storbinary(f"STOR {remoto}", f)
    print(f"  enviado  {local}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    host, usuario = sys.argv[1], sys.argv[2]
    base = (sys.argv[3] if len(sys.argv) > 3 else "www").strip("/")

    lista = [a for a in ARQUIVOS if os.path.exists(os.path.join(RAIZ, a))]
    for pasta in PASTAS:
        for dirpath, _, nomes in os.walk(os.path.join(RAIZ, pasta)):
            for nome in sorted(nomes):
                if nome not in IGNORAR:
                    lista.append(os.path.relpath(os.path.join(dirpath, nome), RAIZ))

    print(f"{len(lista)} arquivos serão enviados para {host}:/{base}/")
    senha = getpass.getpass(f"Senha de FTP de {usuario}: ")
    ftp = conectar(host, usuario, senha)

    raiz_remota = ftp.nlst()
    if base not in [n.strip("/").split("/")[-1] for n in raiz_remota]:
        print(f"A pasta '{base}' não existe na raiz do FTP. Pastas encontradas: {raiz_remota}")
        print("Rode de novo informando a pasta certa como terceiro argumento.")
        ftp.quit()
        sys.exit(2)

    for rel in lista:
        rel = rel.replace(os.sep, "/")
        destino = f"{base}/{rel}"
        garantir_pasta(ftp, os.path.dirname(destino))
        enviar(ftp, rel, destino)

    ftp.quit()
    print("\nPronto. Abra https://cuboit.com.br (se precisar, recarregue com Cmd+Shift+R).")


if __name__ == "__main__":
    main()
