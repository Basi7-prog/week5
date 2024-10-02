#filter amharic letter using Ascii
def clean(row):
    new_data=''
    space=False
    breaker=False
    for a in list(row):
            if((ord(a)>=4608 and ord(a)<=4951) or (ord(a)>=48 and ord(a)<=57)): #with number
            # if((ord(a)>=4608 and ord(a)<=4951)):#without number
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

def clean_repeatitive_words(df,col):
    pattern=r'.*ቴሌግራም.*\n*.*በአዲስ\s*ነገረ\s*ሁሌም\s*ቀዳሚዏች\s*ነን.*\n*'
    df[col]=df[col].str.replace(pattern,'', regex=True)
    return df
        
def tokenize(df,col):
    df['clean data']=df[col].apply(clean)
    return df