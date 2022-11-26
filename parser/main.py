from tag import Tag
from token import Token
from lexer import Lexer
from parser import Parser

# Vinicius Gonçalves de Souza - RA : 119122170
# Mateus Gonçalves de Souza   - RA : 119122458
# Isabela Magalhaes  da Silva - RA: 119123318

'''
Esse eh o programa principal. Basta executa-lo.
'''

if __name__ == "__main__":
   lexer = Lexer('prog1.txt')

   parser = Parser(lexer)

   parser.Programa()

   print("\n=>Tabela de simbolos:")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> Fim da compilacao')
