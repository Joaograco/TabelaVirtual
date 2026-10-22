/*
    Este e o arquivo de configuração do DB.
    Aqui é onde a tabela é criada e configurada
    (talvez um perfil padrão ¯\_(ツ)_/¯)
*/

-- Cria a tabela
create database Tabela;

-- Cria o acesso
create user 'webDB' identified by 'DBpasswd';
grant all on Tabela.* to 'webDB';

-- Cria a tabela de usuários
create table users(
    id int auto_increment primary key,
    user varchar(128) not null,
    nome varchar(1024) not null,
    email varchar(512) not null,
    senha varchar(128) not null,
    sala varchar(32) not null,
    tipo varchar(64) not null
);

-- User default aluno
insert into users (
    user, nome, senha, email, sala, tipo
) values (
    'aluno', 'teste', '$argon2id$v=19$m=65536,t=3,p=4$b7RtYFWaDfUDTs7kQNp2dA$MgGThe+J833clJjHTql9ysTPoJxenBp4da2Au0qll1Q', 'example@aluno', '2c', 'aluno'
);

/*
    User default aluno
    user: aluno
    nome: teste
    senha: aluno
    email: example@aluno
    sala: 1c
    tip: aluno
*/


-- User default prof
insert into users(
    user, nome, senha, email, sala, tipo
) values (
    'prof', 'teste', '51d1e6a398acbda7e15b687de747e7dfe95fa13154dcb40aa8ab37f1e2b393a0', 'example@prof', 'todas', 'prof'
);

/*
    User default professor
    user: prof
    nome: teste
    senha: prof
    email: example@prof
    sala: todas
    tipo: prof
*/