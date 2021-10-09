
%{ 

/*codigo colocado aqui aparece no arquivo gerado pelo flex*/ 

%} 

/* This tells flex to read only one input file */ 
%option noyywrap 

/* definicoes regulares */ 
letter [A-Za-z]
upperCaseLetter [A-Z]
lowerCaseLetter [a-z]
digit [0-9]
separation (" "){2,}
word ({letter}+)
positiveNumber ({digit}+)
negativeNumber ([-]{digit}+)
decimalNumber (([-]{digit}+[.]{digit}+)|({digit}+[.]{digit}+))
phoneNumber ({digit}{4}[-]{digit}{4})
fullName (({upperCaseLetter})({lowerCaseLetter}+)([ \n\t\r]{1}|$)){3,4}
carPlate ({upperCaseLetter}{3}[-]{digit}{4})
delim		[ \t\n]
ws		{delim}+






%% 

{positiveNumber} {printf("Foi encontrado um numero inteiro positivo. LEXEMA: %s\n", yytext);}
{negativeNumber} {printf("Foi encontrado um numero inteiro negativo. LEXEMA:: %s\n", yytext);}
{phoneNumber} {printf("Foi encontrado um telefone. LEXEMA:: %s\n", yytext);}
{fullName} {printf("Foi encontrado um nome completo. LEXEMA:: %s\n", yytext);}
{decimalNumber} {printf("Foi encontrado um numero com parte decimal. LEXEMA: %s\n", yytext);}
{word} {printf("Foi encontrado uma palavra. LEXEMA: %s\n", yytext);}
{carPlate} {printf("Foi encontrado uma placa. LEXEMA: %s\n", yytext);}
{ws}		{/*nenhuma acao e nenhum retorno*/} 




%% 

/*codigo em C. Foi criado o main, mas podem ser criadas outras funcoes aqui.*/ 

int main(void) 
{ 
    /* Call the lexer, then quit. */ 
    yylex(); 
    return 0; 
}
