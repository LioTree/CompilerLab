#include<stdio.h> 
#include<stdlib.h>
#include<string.h>
#include<conio.h>

#define MAXLEXEME 100 //lexeme最大长度
#define MAXCHAR 999999 //源程序字符限制，偷个懒

enum symbol{
    NUL,IDENT,NUMBER,PLUS,MINUS, // 不能识别的字符 标识符 数字 + -
    TIMES,SLASH,ODDSYM,EQL,NEQ,  // * / odd = <>
    LSS,LEQ,GTR,GEQ,LPAREN, // < <= > >= (
    RPAREN,COMMA,SEMICOLON,PERIOD,BECOMES,HASH, // ) , ; . := #
    BEGINSYM,ENDSYM,IFSYM,THENSYM,WHILESYM, // begin end if then while
    WRITESYM,READSYM,DOSYM,CALLSYM,CONSTSYM,VARSYM,PROCSYM, // write read do call const var procedure
    END //自己加一个代表EOF的END类型
};

//单字符转symbol，通过init_char_symbol
int char_symbol[128] = {NUL};

//symbol对应的文本
char symbol_text[][15] = {
    "NUL","IDENT","NUMBER","PLUS","MINUS", // 不能识别的字符 标识符 数字 + -
    "TIMES","SLASH","ODDSYM","EQL","NEQ",  // * / odd = <>
    "LSS","LEQ","GTR","GEQ","LPAREN", // < <= > >= (
    "RPAREN","COMMA","SEMICOLON","PERIOD","BECOMES","HASH", // ) , ; . :=
    "BEGINSYM","ENDSYM","IFSYM","THENSYM","WHILESYM", // begin end if then while
    "WRITESYM","READSYM","DOSYM","CALLSYM","CONSTSYM","VARSYM","PROCSYM", // write read do call const var procedure
    "END" //自己加一个代表EOF的END类型
};

//按字母顺序排列的保留字
char keywords [][15] = {"begin", "call", "const", "do", "end", "if", "procedure", "read", "then", "var", "while", "write"};
//按字母顺序排列的保留字symbol
int keywords_symbol [15] = {BEGINSYM, CALLSYM, CONSTSYM, DOSYM, ENDSYM, IFSYM, PROCSYM, READSYM, THENSYM, VARSYM, WHILESYM, WRITESYM};

struct token{
    enum symbol s;  //符号类型
    char lexeme[MAXLEXEME];   //符号的值，不需要时为""
};

int line=1; //记录已经读了多少行，用于错误处理

//初始化init_char_symbol
void init_char_symbol(){
    char_symbol['+'] = PLUS;
    char_symbol['-'] = MINUS;
    char_symbol['*'] = TIMES;
    char_symbol['/'] = SLASH;
    char_symbol['='] = EQL;
    // 这两个在 <> <= >= 那里就弄完了
    // char_symbol['<'] = LSS;
    // char_symbol['>'] = GTR;
    char_symbol['('] = LPAREN;
    char_symbol[')'] = RPAREN;
    char_symbol[','] = COMMA;
    char_symbol[';'] = SEMICOLON;
    char_symbol['.'] = PERIOD;
    char_symbol['#'] = HASH;
}

//二分搜索关键字
int search_keywords(char *target){
    int n = sizeof(keywords) / sizeof(keywords[0]);
    int low = 0;
	int high = n - 1;
	int middle;
    int result;

	while (1)
	{
		middle = (low + high) / 2;
        result = strcmp(keywords[middle],target);

		if ( result == 0 )
			return middle;
		else if ( n <= 0 )
			return -1;
		else if ( result > 0 )
			high = middle - 1;
		else if ( result < 0 )
			low = middle + 1;
		n = high - low;
	}
}

struct token getsym(){
    struct token result = {NUL,""};
    char ch;
    char temp[MAXLEXEME] = ""; //temp 
    int index; //后面判断标识符和保留字的时候用

    memset(temp,'\0',strlen(temp)); //方便往后面添字符

    //过滤空白字符
    do{
        ch = getchar();
        if( ch == '\n'){
            line++;
        }
    }
    while( ch == ' ' || ch == '\n' || ch == '\r' || ch == '\t' );
    
    temp[strlen(temp)] = ch;

    //标识符和保留字
    if( ( ch >= 'a' && ch <= 'z' ) || ( ch >= 'A' && ch <= 'Z' ) || ( ch == '_' ) ){ //标识符和保留字第一个字符
        ch = getchar();
        //标识符和保留字后面的字符
        while( ( ch >= 'a' && ch <= 'z' ) || ( ch >= 'A' && ch <= 'Z' ) || ( ch == '_' ) || ( ch >= '0' && ch <= '9' ) ){
            temp[strlen(temp)] = ch;
            ch = getchar();
        }
        ungetc(ch,stdin); //最后一个字符不是标识符或保留字的内容，扔回去

        if( ( index = search_keywords(temp) ) != -1){
            result.s = keywords_symbol[index];
        }
        else{
            result.s = IDENT;
        }
        strcpy(result.lexeme,temp);
    }

    //数字
    else if( ch >= '0' && ch <= '9' ){
        ch = getchar();
        while( (ch >= '0' && ch <= '9') ){
            temp[strlen(temp)] = ch;
            ch = getchar();
        }
        ungetc(ch,stdin); //最后一个字符不是数字的内容，扔回去

        result.s = NUMBER;
        strcpy(result.lexeme,temp);
    }

    //:=
    else if( ch == ':' ){
        ch = getchar();
        if( ch == '=' ){
            result.s = BECOMES;
            temp[strlen(temp)] = ch;
            strcpy(result.lexeme,temp);
        }
        else{
            ungetc(ch,stdin); //最后一个字符不是=，扔回去
        }
    }

    //<> <=
    else if( ch == '<' ){
        ch = getchar();
        if( ch == '>' ){
            result.s = NEQ;
            temp[strlen(temp)] = ch;
        }
        else if( ch == '=' ){
            result.s = LEQ;
            temp[strlen(temp)] = ch;
        }
        else{
            result.s = LSS;
            ungetc(ch,stdin); //最后一个字符不是>或=，扔回去
        }
        strcpy(result.lexeme,temp);
    }

    //>=
    else if( ch == '>' ){
        ch = getchar();
        if( ch == '=' ){
            result.s = GEQ;
            temp[strlen(temp)] = ch;
        }
        else{
            ungetc(ch,stdin); //最后一个字符不是=，扔回去
        }
        strcpy(result.lexeme,temp);
    }

    // + - * / = ( ) , ; .
    else if( ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '=' || 
             ch == '(' || ch == ')' || ch == ',' || ch == ';' || ch == '.' || ch == '#'){
        result.s = char_symbol[ch];
        strcpy(result.lexeme,temp);
    }

    else if( ch == EOF ){
        result.s = END;
        strcpy(result.lexeme,temp);
    }

    //其他不可识别字符
    else{
        //result.s默认就是NUL，但还是设一下
        result.s = NUL;
        strcpy(result.lexeme,temp);
    }

    return result;
}

//去除注释
void strip_comment(char *filename1,char *filename2){
     FILE *fp1 = NULL;
     FILE *fp2 = NULL;
     char buffer[MAXCHAR];
     char buffer2[MAXCHAR] = {'\0'};
     
     fp1 = fopen(filename1, "r");
     fp2 = fopen(filename2, "w");

     //c是真滴麻烦
     fseek(fp1,0,SEEK_END);
     int filesize = ftell(fp1);//通过ftell函数获得指针到文件头的偏移字节数
     rewind(fp1);
     fread(buffer,1,filesize,fp1);
     rewind(fp1);

     int j=0;
     for(int i=0;i<strlen(buffer);i++){
         if( buffer[i] == '/' && buffer[i+1] == '*' ){
             i+=2;
             while( buffer[i] != '*' && buffer[i+1] != '/' ){
                 i++;
             }
             i+=2;
         }

         if(buffer[i] == '{'){
             i++;
             while( buffer[i] != '}' ){
                 i++;
             }
             i++;
         }
         buffer2[j] = buffer[i];
         j++;
     }
     fwrite(buffer2,1,strlen(buffer2),fp2);
     rewind(fp2);
}

int main(){
   
    // char *filename1 = "test.pl0"; //源程序
    char *filename1 = "test2.pl0"; //源程序
    char *filename2 = "temp.pl0"; //去除注释后
    struct token result;

    strip_comment(filename1,filename2);

    freopen(filename2,"r",stdin);    //重定向
    init_char_symbol();

    while(1) {
        result = getsym(filename2);
        if( result.s == END ){
            break;
        }
        if( result.s == NUL ){
            printf("unexpected char '%s' in line %d\n",result.lexeme,line);
            // break;
        }
        printf("(%s,%s)\n",symbol_text[result.s],result.lexeme);
    }
    getch();

    return 0;
}