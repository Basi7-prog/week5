#filter amharic letter using Ascii
def clean(row):
    new_data=''
    for a in list(row):
            # if((ord(a)>=4608 and ord(a)<=4951) or (ord(a)>=48 and ord(a)<=57) or ord(a)==32): #with number
            if((ord(a)>=4608 and ord(a)<=4951) or ord(a)==32):#without number
                new_data+=a
    return new_data


def tokenize(df,col):
    df['clean data']=df[col].apply(clean)
    return df