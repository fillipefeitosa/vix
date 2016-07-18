-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2016-03-15 02:36:03.547




-- tables
-- Table: Copa
CREATE TABLE Copa (
    copa_Ano date  NOT NULL,
    copa_Inicio date  NOT NULL,
    copa_Fim date  NOT NULL,
    copa_Cidade char(30)  NOT NULL,
    CONSTRAINT Copa_pk PRIMARY KEY (copa_Ano)
);



-- Table: Equipe
CREATE TABLE Equipe (
    equipe_ID int  NOT NULL,
    treinador_ID int  NOT NULL,
    CONSTRAINT Equipe_pk PRIMARY KEY (equipe_ID)
);



-- Table: Equipe_Copa_Ano
CREATE TABLE Equipe_Copa_Ano (
    Copa_copa_Ano date  NOT NULL,
    País_Sigla char(3)  NOT NULL,
    Equipe_equipe_ID int  NOT NULL
);



-- Table: Equipe_Jogador
CREATE TABLE Equipe_Jogador (
    Equipe_equipe_ID int  NOT NULL,
    Pessoa_pessoa_ID int  NOT NULL
);



-- Table: Jogo
CREATE TABLE Jogo (
    jogo_ID int  NOT NULL,
    jogo_Data date  NOT NULL,
    jogo_Hora time  NOT NULL,
    Copa_copa_Ano date  NOT NULL,
    jogo_Estadio char(20)  NOT NULL,
    CONSTRAINT Jogo_pk PRIMARY KEY (jogo_ID)
);



-- Table: Jogo_Equipes
CREATE TABLE Jogo_Equipes (
    Jogo_jogo_ID int  NOT NULL,
    Equipe_equipe_ID int  NOT NULL,
    Equipe_Gols int  NOT NULL
);



-- Table: País
CREATE TABLE País (
    Sigla char(3)  NOT NULL,
    pais_Nome char(30)  NULL,
    CONSTRAINT Sigla PRIMARY KEY (Sigla)
);



-- Table: Pessoa
CREATE TABLE Pessoa (
    pessoa_ID int  NOT NULL,
    pessoa_Nome char(30)  NOT NULL,
    pessoa_dataNascimento date  NOT NULL,
    País_Sigla char(3)  NOT NULL,
    CONSTRAINT Pessoa_pk PRIMARY KEY (pessoa_ID)
);







-- foreign keys
-- Reference:  Equipe_Copa_Ano_Copa (table: Equipe_Copa_Ano)

ALTER TABLE Equipe_Copa_Ano ADD CONSTRAINT Equipe_Copa_Ano_Copa 
    FOREIGN KEY (Copa_copa_Ano)
    REFERENCES Copa (copa_Ano)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Equipe_Copa_Ano_Equipe (table: Equipe_Copa_Ano)

ALTER TABLE Equipe_Copa_Ano ADD CONSTRAINT Equipe_Copa_Ano_Equipe 
    FOREIGN KEY (Equipe_equipe_ID)
    REFERENCES Equipe (equipe_ID)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Equipe_Copa_Ano_País (table: Equipe_Copa_Ano)

ALTER TABLE Equipe_Copa_Ano ADD CONSTRAINT Equipe_Copa_Ano_País 
    FOREIGN KEY (País_Sigla)
    REFERENCES País (Sigla)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Equipe_Jogador_Pessoa (table: Equipe_Jogador)

ALTER TABLE Equipe_Jogador ADD CONSTRAINT Equipe_Jogador_Pessoa 
    FOREIGN KEY (Pessoa_pessoa_ID)
    REFERENCES Pessoa (pessoa_ID)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Equipe_Pessoa (table: Equipe)

ALTER TABLE Equipe ADD CONSTRAINT Equipe_Pessoa 
    FOREIGN KEY (treinador_ID)
    REFERENCES Pessoa (pessoa_ID)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Jogo_Copa (table: Jogo)

ALTER TABLE Jogo ADD CONSTRAINT Jogo_Copa 
    FOREIGN KEY (Copa_copa_Ano)
    REFERENCES Copa (copa_Ano)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Pessoa_País (table: Pessoa)

ALTER TABLE Pessoa ADD CONSTRAINT Pessoa_País 
    FOREIGN KEY (País_Sigla)
    REFERENCES País (Sigla)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Table_10_Equipe (table: Equipe_Jogador)

ALTER TABLE Equipe_Jogador ADD CONSTRAINT Table_10_Equipe 
    FOREIGN KEY (Equipe_equipe_ID)
    REFERENCES Equipe (equipe_ID)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Table_13_Equipe (table: Jogo_Equipes)

ALTER TABLE Jogo_Equipes ADD CONSTRAINT Table_13_Equipe 
    FOREIGN KEY (Equipe_equipe_ID)
    REFERENCES Equipe (equipe_ID)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;

-- Reference:  Table_13_Jogo (table: Jogo_Equipes)

ALTER TABLE Jogo_Equipes ADD CONSTRAINT Table_13_Jogo 
    FOREIGN KEY (Jogo_jogo_ID)
    REFERENCES Jogo (jogo_ID)
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE 
;






-- End of file.

