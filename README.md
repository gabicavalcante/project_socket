# AuthSockets 

Projeto Python utilizando socket para a comunicação entre Cliente TCP, Servidor de Autenticação TCP e Proxy TCP. 
A arquitetura alto nível do projeto é apresentada abaixo. 

![Arquitetura](https://github.com/I-am-Gabi/project_socket/blob/master/static/arquitetura.png)

O cliente se comunica com o servidor de autenticação passando seu email e senha, e recebe como uma resposta um token, que deve ser usado a cada requisição a um serviço. 
Após estar autenticado, ele tentará acessar um SP, que estará protegido por um proxy que intercepta a requisição e dá o acesso somente se o token for válido. 


## Requirements

## Protocol
 
Cliente - Servidor de Autenticação
```
C: HELO  
S: 250 HELO ('127.0.0.1', 59893)
C: AUTH EMAIL:gabicavalcantesilva@gmail.com PASSWORD:12345
S: 200 TOKEN eyJzYWx0IjogIjM2MTU1OS
C: BYE

Cliente - Proxy 
C: HELO
S: 250 HELO ('127.0.0.1', 59895)
C: SELECT_PROJECTS TOKEN eyJzYWx0IjogIjM2MTU1OS
S: {u'_id': ObjectId('58e59a1f3a140e226e1eb580'), u'name': u'project01', u'description': u'TEST'}, {u'_id': ObjectId('58e59a1f3a140e226e1eb581'), u'name': u'project02', u'description': u'TEST'}, {u'_id': ObjectId('58e59a1f3a140e226e1eb582'), u'name': u'project03', u'description': u'TEST'}
C: BYE  `
```
