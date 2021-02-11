# EJ Bot




# Primeiros passos

```
make first-run
```


# Fluxo de trabalho

Para realizar o treinamento e criar os modelos necessários para conversa do bot é realizado o comando:

```
make train
```

Para utilização do bot em terminal há o comando

```
make run-shell
```


Listagem e documentação dos comandos make disponíveis:

```
make help
```

# Rasa Boilerplate

A estrutura desse projeto foi baseada na [documentação do rasa](https://rasa.com/docs/rasa/) e [também no boilerplate](https://github.com/lappis-unb/rasa-ptbr-boilerplate).


# Executando testes

A execução de testes também é realizada por meio de comandos make, listados a seguir:

- make test
- make run-test-nlu
- make run-test-core
- make test-actions


# Estrutura básica do projeto

Abaixo, segue em destaque na estrutura de pastas os arquivos que serão mais utilizados durante o desenvolvimento, para que haja evolução da interface conversacional do bot. Nota-se que é importante seguir o padrão de nomeclatura do rasa, para que ele consiga interpretar corretamente os diferentes contextos (por exemplo utter_nome).

```shell
-- bot/ 
    -- actions/
        - actions.py # onde são declaradas ações realizadas pelo bot que vão além de responder o usuário com texto
    -- data/
        - nlu.yml # aqui são definidas as intents, que são as entradas esperadas do usuário
        - rules.yml #
        - stories.yml # cada story é um fluxo que deve ocorrer entre o usuário e o bot
    -- domain.yml # são definidas as utter, respostas do bot que são apenas texto e também  descreve o domínio do bot, que inclue intents, entities, slots, templates e actions que o bot deve ter consciência.
    -- endpoints.yml # arquivo que contém a configuração do webhook para uma ação personalizada
    -- tests/
        - test_stories.yml # testes dos fluxos de conversas
        - test_actions.py # teste das ações e outros recursos, usando pytest
```


