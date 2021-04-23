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



# WebChat

Você pode simular uma conversa com o ejBot a partir de um webchat.

1. Suba o container do nginx que serve a pagina do webchat: `make run-webchat`;
2. Acesse a pagina em `http://localhost:8001/`;

É provável que você precise retreinar o bot, e recriar os containers da API para que a configuração do canal socketio seja aplicada.

Para que seja possível resgatar dados da EJ, é necessário que o endereço que o webchat está
hospedado possua uma conexão com a EJ (Rasa Conversation). Para isso, basta ir na EJ, na conversa que queira conectar, e nela a parte de Ferramentas > Rasa Chatbot. Lá deve ser incluido o endereço, nesse caso, `http://localhost:8001/`.


# Telegram

Para configurar o bot do telegram, é necessário sua criação com o [Fatherbot](https://core.telegram.org/bots#3-how-do-i-create-a-bot). A partir disso, obterá um token e um username, esses
dois devem ser escritos no arquivo `bot/credentials.yml`, substituindo os valores:

```yml
custom_channels.TelegramInputChannel:
  access_token: ${TOKEN_PROVIDED_BY_FATHER_BOT}
  verify: ${BOT_USERNAME}
  webhook_url: "${TELEGRAM_WEBHOOK_URL}"
```

Nesse repositório, foi criado um bot para ambiente de desenvolvimento local, chamado duda_local_bot. Porém, o telegram aceita webhooks apenas que possuem o protocolo HTTPS.
Então para testá-la você pode fazer o download e instalação do aplicativo [ngrok](https://ngrok.com/download). Então, vá para o diretório que possui o programa e execute o comando :

```shell
$ ./ngrok http 5006
```
Com isso, será criado um túnel e serão exibidas as seguintes informações no terminal, copie o
endereço https que direciona para o localhost:5006 e o substitua na variável TELEGRAM_WEBHOOK_URL, 
não esquecendo de acrescentar o /webhooks/telegram/webhook ao final da URL (no exemplo ficaria:
**https://10483b5f4.ngrok.io/webhooks/telegram/webhook**):

```shell
ngrok by @inconshreveable                                                                                                             (Ctrl+C to quit)
                                                                                                                                                      
Session Status                online                                                                                                                  
Session Expires               1 hour, 59 minutes                                                                                                      
Update                        update available (version 2.3.39, Ctrl-U to update)                                                                     
Version                       2.3.38                                                                                                                  
Region                        United States (us)                                                                                                      
Web Interface                 http://127.0.0.1:4040                                                                                                   
Forwarding                    http://10483b5f4.ngrok.io -> http://localhost:5002                                                                   
Forwarding                    https://10483b5f4.ngrok.io -> http://localhost:5002                                                                  
                                                                                                                                                      
Connections                   ttl     opn     rt1     rt5     p50     p90                                                                             
                              0       0       0.00    0.00    0.00    0.00                                                                            
                                                                       
```

Informações mais detalhadas das requisições realizadas para o endereço podem ser verificadas em
http://127.0.0.1:4040 .

## Ambientes da duda

Existem 3 bots diferentes da duda, cada um de um ambiente diferente. São eles:

- duda_local_bot: ambiente de desenvolvimento local;
- duda_dev_bot: ambiente de homologação;
- duda_ej_bot: ambiente de produção.

## Interações em grupo

Para que o bot inicie a conversa e fale as instruções, basta dizer um oi, ou enviar /start. Após essa mensagem, o bot dará instruções sobre como prosseguir.

Existe também o comando do telegram /help que lista todos os comandos disponíveis. Atualmente, o único comando disponível é o /participar [ID_CONVERSA]. Quando em conversa privada, o bot já 
inicia com uma conversa pré selecionada por administradores. 

Logo, quando em um grupo, para que haja participação em uma conversa, é necessário que um usuário
selecione um ID de conversa, para que o bot consiga carregá-la.
