# 🔐 Gerador de Senhas Fortes

Um programa simples, feito em Python, que cria senhas **fortes, aleatórias e que nunca se repetem**. Ele não pede nenhum dado seu e não guarda as senhas que cria.

## Por que usar

- **Não pergunta nada sobre você.** Nada de nome, data de nascimento, pet ou time. As senhas são sorteadas, então ninguém consegue adivinhar pensando em você.
- **Não guarda as suas senhas.** Ela aparece na tela, você copia e pronto.
- **Nunca entrega a mesma senha duas vezes** no seu computador.
- **Não precisa instalar nada além do Python.**

## O que você precisa

Só do [Python 3](https://www.python.org/downloads/) instalado. Para saber se você já tem, abra o terminal e digite `python --version` (no Mac e no Linux, `python3 --version`).

## Como usar

1. Clique no botão verde **Code** no topo desta página e depois em **Download ZIP**. Extraia a pasta.
2. Abra o terminal dentro da pasta e rode:

   ```
   python gerador_senha.py
   ```

   (no Mac e no Linux: `python3 gerador_senha.py`)

3. Escolha uma opção no menu:

   | Opção | O que faz |
   |-------|-----------|
   | `1` | Gera uma senha nova |
   | `2` | Muda o tamanho da senha |
   | `3` | Sai do programa |

4. A senha aparece assim:

   ```
   ========================================
     PRONTO! SUA SENHA NOVA:

       uEq*_%a&-q5N7kP!

     Nível: Muito forte
   ========================================
   ```

5. **Copie a senha e guarde num gerenciador de senhas**, como o Bitwarden. Depois aperte Enter e a tela é limpa.

## Como são as senhas

- De **12 a 64 caracteres** (se você não mudar, serão 16)
- Letras **maiúsculas e minúsculas**
- **Números**
- **Símbolos** (`@ # $ ! ? * % & - _ + =`)
- Sem sequências fáceis como `aaa`, `abc` ou `321`

## Sua privacidade e segurança

**O que o programa faz com a sua senha:** mostra na tela uma vez e mais nada. Ela não é salva em arquivo, não é enviada pela internet e não fica registrada em lugar nenhum. O programa funciona totalmente offline.

**O que fica guardado no seu computador:** só uma lista de códigos, um para cada senha que já foi gerada. Ela serve apenas para o programa não repetir senha. Esses códigos não permitem descobrir as senhas. Ela fica aqui:

- Windows: `C:\Users\SeuNome\.gerador_senha\`
- Mac e Linux: `~/.gerador_senha/`

Você pode apagar essa pasta quando quiser. O único efeito é o programa esquecer as senhas que já gerou.

**Algumas dicas para usar com segurança:**

- Guarde as senhas num gerenciador de senhas, nunca num bloco de notas ou numa conversa.
- Gere a senha longe de olhares curiosos, já que ela aparece na tela por alguns instantes.
- Depois de guardar a senha, feche a janela do terminal. Alguns terminais guardam o histórico mesmo depois de limpar a tela.
- Use uma senha diferente para cada site ou aplicativo.

<details>
<summary><b>Detalhes técnicos (para quem tem curiosidade)</b></summary>

- As senhas são sorteadas com o módulo `secrets` do Python, feito para uso em segurança, e não com o `random`.
- Para evitar repetição, o programa transforma cada senha em um código com **PBKDF2-SHA256**, usando 200 mil repetições e um *salt* aleatório gerado na primeira execução. Só o código vai para o registro, nunca a senha.
- O registro fica na pasta pessoal do usuário. No Linux e no Mac, a pasta e o arquivo são criados com acesso apenas para o dono (permissões `700` e `600`).
- O programa só usa a biblioteca padrão do Python, sem dependências externas.

</details>

## Perguntas frequentes

**A senha some depois que aperto Enter?**
Some da tela, e o programa não tem cópia dela. Por isso é importante guardar antes de continuar.

**Posso receber a mesma senha de novo?**
No seu computador, não. O programa confere o registro e sorteia outra se a senha já tiver sido gerada.

**E se eu apagar a pasta `.gerador_senha`?**
Nada grave acontece. O programa só esquece as senhas antigas e cria um registro novo.

**Outra pessoa que use o meu computador consegue ver as minhas senhas?**
Não. Elas não ficam salvas em lugar nenhum. Ela só veria o registro de códigos, que não revela senha nenhuma.

**Posso usar essas senhas de verdade?**
Sim. Elas são aleatórias e fortes. Só lembre de guardá-las com segurança.

## Para quem quer contribuir

Para rodar os testes automáticos:

```
python test_gerador_senha.py
```

Os testes conferem, entre outras coisas, que as senhas nunca repetem, que o registro não guarda a senha, e que o programa não tem nenhuma função para salvar senhas em arquivo. Sugestões e melhorias são bem-vindas.
   
## Limitações

- A garantia de não repetir vale por computador. Para valer entre pessoas diferentes seria preciso um servidor central.
- É um projeto de estudo e prática de segurança. Para o dia a dia, um gerenciador de senhas completo continua sendo a melhor opção.


## Autor

Feito por **Lucas Carlos** ([@LucasCzx](https://github.com/LucasCzx)), desenvolvedor em formação, com foco em cibersegurança.

Este projeto nasceu como um exercício de lógica e segurança: criar senhas realmente aleatórias, sem depender de dados pessoais, e sem nunca guardá-las. Sugestões e dicas são bem-vindas! Se encontrar algum problema ou tiver uma ideia, é só avisar na aba **Issues** do repositório.

**Tecnologias**

- **Uso:** Python, HTML e CSS
- **Em construção:** JavaScript
- **Estudando por fora:** Redes de Computadores, Linux e SQL
