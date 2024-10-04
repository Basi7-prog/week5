import re

def check_amharic_char(chr,multi=False):
    #gets a char and check a only a single character if multi(mlti-line) is false
    if(not multi):
        amharic_cha=False
        
        if(ord(chr)>=4608 and ord(chr)<=4951):
            amharic_cha= True
    
        return amharic_cha
    #gets string and checks for amharic char by iterating one by one if multi(mlti-line) is true
    else:
        for c in list(chr):
            if(check_amharic_char(c)):
                return True
        return False
    

#filter amharic letter using Ascii
def clean(row):
    new_data=''
    space=False
    breaker=False
    for a in list(row):
            if(check_amharic_char(a) or (ord(a)>=48 and ord(a)<=57)): #with number
            # if(check_amharic_char(a)):#without number
                space=True
                breaker=True
                new_data+=a
            elif(a==' ' and space):
                space=False
                new_data+=a
            elif(a=='\n' and breaker):
                breaker=False
                new_data+=a
                
    return new_data

def clean_repeatitive_words(df,col,col2):
    # pattern=r'\n*\s*.*ቴሌግራም.*\n*|\n*\s*.*በአዲስ\s*ነገር\s*ሁሌም\s*(?:ቀዳሚዎች|ቀዳሚዏች)\s*ነን.*\n*|.*\s*(?:የበዓል|የበአል)\s*ቅናሽ\s*.*|.*\n*(?:በዓሉን|በአሉን)\s*ምክንያት\s*በማድረግ\s*.*'
    pattern=r'\n*\s*.*ቴሌግራም.*\n*|\n*\s*.*በአዲስ\s*.*|.*\s*(?:የበዓል|የበአል)\s*ቅናሽ\s*.*|.*\n*(?:በዓሉን|በአሉን)\s*ምክንያት\s*በማድረግ\s*.*|.*\s*ስጦታ (?:አዘጋጅተንልዎታል|አዘጋጅተናል)|መልካም.*|ተጀመረ.*|.*ቅናሽ አድርገናል|.*በፈጣን ሞተረኞቻችን እንልክልዏታለን'
    
    df[col2]=df[col].str.replace(pattern,'', regex=True)
    return df
        
def tokenize(df,col):
    df[col]=df[col].apply(clean)
    return df
#የዘይት
def label(messages):
    first_line,remainings=None,None
    labeled_token=[]
    for message in messages:
        if '\n' in message:
            first_line,remainings=message.split('\n',1)
        else:
            first_line=message.split('\n')
            
        if ' ' in first_line:
            tokens=first_line.split(' ')
            labeled_token.append(f'{tokens[0]} B-PRODUCT')
            for token in tokens[1:]:
                if(check_amharic_char(token,multi=True) or token.isdigit()):
                    labeled_token.append(f'{token} I-PRODUCT')
        if '\n' in remainings:
            # lines=remainings.split('\n')
            price_pattern=r'በ\s*\n*(?!09)\d{2,}|\d+\s*ብር|ብር\s*(?!09\d*)\d+'
            match=re.findall(price_pattern,remainings)
            if(len(match)>0):
                # price=match.group().replace('\n','')
                price=' '.join(match).replace('\n','')
                labeled_token.append(f'{price} I-PRICE')
            # for line in lines:
            #     labeled_token.append(f'{line} I-PRICE')
                # match=re.search(price_pattern,line)
                # if(match):
                #     labeled_token.append(f'{match.group()} I-PRICE')
                # else:
                #     labeled_token.append(f'{match.group()} NO-PRICE')
    
    with open('output.txt','w',encoding='utf-8') as file:
        file.write('\n'.join(labeled_token))
        
    # print(labeled_token)
        