1.0 Instanciar um script asgi

2.0 -> Ativar o wsl do debian via powershell

2.1 -> Atualizar o sistema debian
    sudo apt update && sudo apt upgrade -y

2.2 Instalar ependencias de HTTP e assinaturas
    sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

3.0 -> Adicionar a chave GPG oficial do docker
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

3.1 instalar o docker no wsl debian
    sudo apt --install docker
    

