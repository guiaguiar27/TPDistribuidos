
%{ 

/*codigo colocado aqui aparece no arquivo gerado pelo flex*/ 

%} 

/* This tells flex to read only one input file */ 
%option noyywrap 

/* definicoes regulares */ 
letter [A-Za-z]
upperCaseLetter [A-Z]
lowerCaseLetter [a-z]
letterOrNumber [a-zA-Z0-9]
digit [0-9]
cpf ((({digit}{3}[.]){2}){digit}{3}[-]{digit}{2})
cnpj ({digit}{2}[.]{digit}{3}[.]{digit}{3}[/]{digit}{4}[-]{digit}{2})
email ({letterOrNumber}+("@"){letterOrNumber}+([.][a-zA-z]+){0,2})
dolar (("$"){digit}+[.]{digit}{1,2})
real (("R$"){digit}+[.]{digit}{1,2})
euro (("€"){digit}+[.]{digit}{1,2})
libra (("£"){digit}+[.]{digit}{1,2})

delim		[ \t\n]
ws		{delim}+






%% 



{cpf} {printf("Foi encontrado um cpf. LEXEMA:: %s\n", yytext);}
{cnpj} {printf("Foi encontrado um cnpj. LEXEMA:: %s\n", yytext);}
{dolar} {printf("Foi encontrado um valor em dolar. LEXEMA:: %s\n", yytext);}
{real} {printf("Foi encontrado um valor em real. LEXEMA:: %s\n", yytext);}
{euro} {printf("Foi encontrado um valor em euro. LEXEMA:: %s\n", yytext);}
{libra} {printf("Foi encontrado um valor em libra. LEXEMA:: %s\n", yytext);}
{email} {printf("Foi encontrado um email. LEXEMA:: %s\n", yytext);}
{ws}		{/*nenhuma acao e nenhum retorno*/} 




%% 

/*codigo em C. Foi criado o main, mas podem ser criadas outras funcoes aqui.*/ 

int main(void) 
{ 
    /* Call the lexer, then quit. */ 
    yylex(); 
    return 0; 
}
