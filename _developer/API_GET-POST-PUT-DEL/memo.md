0 -> Instala uma distro
    wsl --install <distro_name>

I -> Altera entre distros
    wsl --set-default <distro_name>

II -> Ativar distro
    wsl -d <distro_name>

III -> Desativar uma distro especifica
    wsl --terminate <distro_name>

IV -> Retorna os wsl ativos 
    wsl -l -v 

V -> Retorna processos wsl ativos no windows e quanto de processamento estão consumindo
    Get-Process wslhost, vmmem, vmmemWSL -ErrorAction SilentlyContinue

VI -> Desativar todas as distros
    wsl --shutdown


VII -> Alterar a versão do wsl
    wsl --set-version <distro_name>
