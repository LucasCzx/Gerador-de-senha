# Gerador de Senhas Fortes

Projeto em Python feito para praticar lógica e segurança. Não precisa instalar nenhuma biblioteca.

O programa **não pergunta nada sobre você**. Ele só cria senhas aleatórias, fortes e que nunca se repetem.

## O que as senhas têm

- de 8 a 64 caracteres (o padrão é 12)
- letras maiúsculas e minúsculas
- números
- caracteres especiais (@ # $ ! ? * % & - _ + =)
- nada de sequências fáceis, como `aaa`, `abc` ou `321`

Como as senhas são sorteadas, elas não têm relação nenhuma com nome, datas, pets, parentes ou times.

## Como rodar

```
python gerador_senha.py
```

Escolha `1` para gerar uma senha, `2` para mudar o tamanho e `3` para sair.

## Onde aparece a senha

Ao escolher `1`, a senha aparece **na tela do terminal**, assim:

```
========================================
  SUA SENHA:

    uEq*_%a&-q5N

  Nível: Forte
========================================
```

Depois o programa pergunta se você quer salvar a senha em um arquivo de texto. Se responder `s`, ele pergunta para que é a senha (por exemplo, "Instagram") e salva em `minhas_senhas.txt`, mostrando o caminho completo do arquivo. Se responder `n`, a senha não fica guardada em lugar nenhum, então anote.

Cuidado: quem abrir o `minhas_senhas.txt` consegue ver as senhas. Guarde esse arquivo em um lugar seguro.

## Como evitar senhas iguais

1. O programa sorteia uma senha usando o módulo `secrets` (aleatoriedade própria para segurança).
2. Transforma a senha em um código (hash SHA-256).
3. Procura esse código no arquivo `registro_codigos.txt`.
4. Se o código já existir, descarta a senha e sorteia outra.
5. Se não existir, guarda o código no arquivo e entrega a senha.

O `registro_codigos.txt` é um arquivo interno do programa. Ele guarda só os **códigos**, nunca as senhas, então abrir ele não mostra nenhuma senha. Não apague esse arquivo, senão o programa esquece o que já gerou.

## Testes

```
python test_gerador_senha.py
```

## Arquivos

- `gerador_senha.py`: o programa
- `test_gerador_senha.py`: os testes
- `registro_codigos.txt`: interno, só com códigos (criado sozinho)
- `minhas_senhas.txt`: só existe se você pedir para salvar uma senha
- `README.md`: este arquivo

## Limitações

- A garantia de não repetir vale para quem usa o **mesmo** arquivo `registro_codigos.txt`. Em computadores separados, cada um teria o seu registro. Para vários computadores seria preciso um banco de dados central.
- Se o `registro_codigos.txt` for apagado, o programa esquece as senhas antigas.
- O arquivo `minhas_senhas.txt` guarda as senhas como texto normal, sem proteção. O ideal para guardar senhas é um gerenciador de senhas.
