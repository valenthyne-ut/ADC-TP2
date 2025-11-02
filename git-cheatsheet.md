# Cábulas

Um conjunto de comandos que muito provavelmente irão ser muito utilizados.

```sh
# Clonar este repositório
git clone https://github.com/valenthyne-ut/ADC-TP2



# Adicionar todas as alterações ao commit
git add .



# Submeter um commit ao ramo
# Este comando abre o editor configurado aos commits.
git commit

# extra para o comando acima; 
# configurar o editor da mensagem para o VSCode
git config --global core.editor code --wait



# Enviar alterações do ramo para o repositório remoto
git push

# Poderá ocorrer um erro que explicita que no repositório remoto
# não existe o ramo no repositório remoto; neste caso é simplesmente
# repetir o push com o seguinte argumento:
git push --set-upstream origin NOME_DO_RAMO



# Criar um novo ramo
git checkout -b NOME_DO_RAMO



# Navegar para um ramo existente
git checkout NOME_DO_RAMO



# Apagar um ramo 
# (não o fazer neste projeto, por indicação do professor)
git branch -D NOME_DO_RAMO
```
