import sys
from LexicalAnalysis import Lexer, Token

if __name__=="__main__":
    print(sys.argv)
    if len(sys.argv) <= 1:
        print("Please provide path to pascal source file")
        exit()

    INPUT_FILE = sys.argv[1]

    text = ""
    with open(INPUT_FILE, 'r') as pascal_file:
        text = "".join(pascal_file.readlines())
    print("Input File Loaded")


    lexer = Lexer(text)
    token = lexer.get_next_token()

    with open("./outputs/pascal_tokens.csv", 'w') as token_file:
        while token.type != Token.EOF:
            # print(token)
            token_file.write(f"{token.type}, {token.value}, {token.line_no}, {token.col_no}\n")
            token = lexer.get_next_token()
    print("Tokens Generated in Outputs folder")    
    
    with open("./outputs/symbol_table.csv", 'w') as symbol_table_file:
        for identifer, id_type in lexer.update_symbol_table().items():
            symbol_table_file.write(f"{identifer}, {id_type}\n")

    print("Symbol Table Generated in Outputs Folder")
