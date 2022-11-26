import sys

from tag import Tag
from token import Token
from lexer import Lexer

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
      if self.token is None: # erro no Lexer
        sys.exit(0)

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")
      sys.exit(0)

   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
      if self.token is None: # erro no Lexer
        sys.exit(0)

   # verifica token esperado t 
   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False

   """
   ATENCAO:
   Procure as marcacoes [TODO] para saber onde e o que fazer.
   """

   # Programa -> CMD EOF
   def Programa(self):
      self.Cmd()
      if(self.token.getNome() != Tag.EOF):
         self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")

   def Cmd(self):
      # Cmd -> if E then { CMD } CMD’
      if(self.eat(Tag.KW_IF)): 
         self.E()
         if(not self.eat(Tag.KW_THEN)):
            self.sinalizaErroSintatico("Esperado \"then\", encontrado " + "\"" + self.token.getLexema() + "\"")
         if(not self.eat(Tag.SMB_AC)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FC)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.CmdLinha()
      # Cmd -> print T;
      elif(self.eat(Tag.KW_PRINT)):
        self.T()
        if(not self.eat(Tag.SMB_PV)):
            self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
      # Cmd -> ATRIB CMD
      else:
         self.Atrib()
         self.Cmd()

   def CmdLinha(self):
      # CmdLinha -> else { CMD }
      if(self.eat(Tag.KW_ELSE)):
         if(not self.eat(Tag.SMB_AC)):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
         self.Cmd()
         if(not self.eat(Tag.SMB_FC)):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
      # CmdLinha -> epsilon
      else:
         return

   # id = T;
   def Atrib(self):
      if(not((self.eat(Tag.KW_ELSE) == self.T()) or self.eat(Tag.OP_ATRIB) or self.eat(Tag.SMB_PV) )):
             self.sinalizaErroSintatico("Esperado \"numero, id \", encontrado "  + "\"" + self.token.getLexema() + "\"")
   

   # E -> T E'
   def E(self):
      if(
         self.T()):
            self.sinalizaErroSintatico("Esperado \"numero, id, aqui\", encontrado " + "\"" + self.token.getLexema() + "\"")
      if(self.ELinha()):
            self.sinalizaErroSintatico("Esperado \">, <, >=, <=, ==, !=, numero, id\", encontrado " + "\"" + self.token.getLexema() + "\"")

   # E -> OP T | Ɛ
   def ELinha(self):
      if(
         self.Op()):
            self.sinalizaErroSintatico("Esperado \">, <, >=, <=, ==, !=, numero, id\", encontrado " + "\"" + self.token.getLexema() + "\"")
      if(self.T()):
             self.sinalizaErroSintatico("numero, id\", encontrado" + "\"" + self.token.getLexema() + "\"")
      

   # Op -> ">" | "<" | ">=" | "<=" | "==" | "!="
   def Op(self):
      if(not(
         self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or 
         self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE) or self.eat(Tag.OP_ATRIB) )):
            self.sinalizaErroSintatico("Esperado \">, <, >=, <=, ==, !=, =\", encontrado " + "\"" + self.token.getLexema() + "\"")

   # T -> id | num
   def T(self):
      if(not(self.eat(Tag.ID) or self.eat(Tag.NUM) or self.eat(Tag.OP_ATRIB) )):
         self.sinalizaErroSintatico("Esperado \"numero, id\", encontrado "  + "\"" + self.token.getLexema() + "\"")
