class Error(Exception): # for generating error
    pass

# constants
AND = "Λ"
OR = "V"
CROSS = "X"
NATURAL = "⋈"
UNION = "U"
LEFTOUTER = "⟕"
RIGHTOUTER = "⟖"
FULLOUTER = "⟗"
INTERSECT = "∩"
MINUS = "-"
setoperantion = ["union","intersect","minus"]
join = ["cross","natural","leftouter","rightouter","fullouter"]

def relation(attribute,tablename): # print normal relation without condition 
    print("∏ ",end="")
    print(','.join([str(x) for x in attribute]) + " ",end="")
    print("(" + (" " + CROSS + " ").join([str(x) for x in tablename]) + ")",end="")
    return

def relation2(attribute,tablename): # for printing join query
    print("∏ ",end="")
    print(','.join([str(x) for x in attribute]) + " ",end="")
    print("(" + tablename + ")",end="")
    return

def relation3(attribute,tablename,condition): # print normal relation with condition
    print("∏",end="")
    print(" " + ','.join([str(x) for x in attribute]) + " ",end="")
    print("(",end="")
    print("σ ",end="")
    print(' '.join([str(x) for x in condition]) + " ",end="")
    print("(" + (" " + CROSS + " ").join([str(x) for x in tablename]) + ")",end="")
    print(")",end="")
    return

def getAttribute(sql): # to get attribute
    return sql.split(" ")[1].split(",")

def getTablename(sql): # to get table names
    return sql.split(" ")[3].split(",")

def getCondition(sql): # to get conditions
    ls = sql.split(" ")
    if(len(ls) > 4 and (ls[4].casefold() == "where")):
        ls2 = []
        for s in ls[5:]:
            if(s.casefold() == "and"): ls2.append(AND)
            elif(s.casefold() == "or"): ls2.append(OR)
            else: ls2.append(s)
        return ls2
    else:
        return list()

def decomposs(sql):  # it will decomposs the string in the list of [attribute,tablename,condition]
    ls = sql.split(" ")
    # print(ls)
    if((len(ls) > 3) and (ls[0].casefold() == "select") and (ls[2].casefold() == "from")):
        ls2 = [getAttribute(sql),getTablename(sql)]
        if(len(getCondition(sql)) > 0): ls2.append(getCondition(sql))
        return ls2
    return list()

def isJoin(sql): # it will find if the query is of join type and if yes then decomposs it
    ls = sql.split(" ")
    # print(ls)
    if(len(ls) > 6 and (ls[4].casefold() in join) and (ls[5].casefold() == "join")):
        ls2 = [decomposs(sql)]
        if(ls[4].casefold() == join[0]): ls2.append(CROSS)
        elif(ls[4].casefold() == join[1]): ls2.append(NATURAL)
        elif(ls[4].casefold() == join[2]): ls2.append(LEFTOUTER)
        elif(ls[4].casefold() == join[3]): ls2.append(RIGHTOUTER)
        else: ls2.append(FULLOUTER)
        ls2.append(ls[6])
        return ls2
    return list()

def isSetoperation(sql): # it will find if the query is of set type and if yes then decomposs it 
    ls = sql.split(" ")
    # print(ls)
    if(len(ls) > 8 and (ls[4].casefold() in setoperantion) and (len(' '.join([str(x) for x in ls[0:4]])) > 0) and (len(' '.join([str(x) for x in ls[5:]])) > 0)):
        ls1 = [decomposs(' '.join([str(x) for x in ls[0:4]]))]
        if(ls[4].casefold() == setoperantion[0]): ls1.append(UNION)
        elif(ls[4].casefold() == setoperantion[1]): ls1.append(INTERSECT)
        else: ls1.append(MINUS)
        ls1.append(decomposs(' '.join([str(x) for x in ls[5:]])))
        return ls1
    return list()

def query(sql): # converting sql to relational algebra

    if(sql[-1] != ';'):
        print("Invalid Query")
        return
    sql = sql[0:len(sql) - 1]

    print("SQL query          : " + sql)
    print("Relational Algebra : ",end="")
    
    ls1 = isSetoperation(sql)
    ls2 = isJoin(sql)
    ls3 = decomposs(sql)
    
    # print(ls1)
    # print(ls2)
    # print(ls3)
    
    if(len(ls1) > 0):
        relation(ls1[0][0], ls1[0][1])
        print(" " + ls1[1],end=" ")
        relation(ls1[2][0], ls1[2][1])
    elif(len(isJoin(sql)) > 0):
        relation2(ls2[0][0],(str(ls2[0][1][0] + " " + str(ls2[1]) + " " + str(ls2[2]))))
    else:
        if(len(ls3) == 2):
            relation(ls3[0], ls3[1])
        elif(len(ls3) == 3):
            relation3(ls3[0], ls3[1], ls3[2])
        else:
            print("Invalid Query")
            return
    print()

# this comment for checking code is correct or not
sql = "select name,age,marks from student;"; query(sql)
sql = "select name,age,marks from student where marks>=85 or cgpi>=7.5 and age<=20 and branch='CSE';"; query(sql)
sql = "select rollno,name,age,marks,cgpi from student,grade;"; query(sql)
sql = "select rollno,name,age,marks,cgpi from student,grade where marks>=85 or cgpi>=7.5 and age<=20 and branch='CSE';"; query(sql)
sql = "select empid,name,salary from employee cross join data;"; query(sql)
sql = "select empid,name,salary from employee natural join data;"; query(sql)
sql = "select empid,name,salary from employee leftouter join data;"; query(sql)
sql = "select empid,name,salary from employee rightouter join data;"; query(sql)
sql = "select empid,name,salary from employee fullouter join data;"; query(sql)
sql = "select customerid,name,bill from customer union select productid,price from product;"; query(sql)
sql = "select customerid,name,bill from customer intersect select productid,price from product;"; query(sql)
sql = "select customerid,name,bill from customer minus select productid,price from product;"; query(sql)

# types of query
# select name,age,marks from student;
# select name,age,marks from student where marks>=85 or cgpi>=7.5 and age<=20 and branch='CSE';
# select rollno,name,age,marks,cgpi from student,grade;
# select rollno,name,age,marks,cgpi from student,grade where marks>=85 or cgpi>=7.5 and age<=20 and branch='CSE';
# select empid,name,salary from employee cross join data;
# select empid,name,salary from employee natural join data;
# select empid,name,salary from employee leftouter join data;
# select empid,name,salary from employee rightouter join data;
# select empid,name,salary from employee fullouter join data;
# select customerid,name,bill from customer union select productid,price from product;
# select customerid,name,bill from customer intersect select productid,price from product;
# select customerid,name,bill from customer minus select productid,price from product;

while(True):
    c = int(input("\n1 - Query\n2 - Exit\n\nEnter your choice : "))
    if(c == 1):
        sql = input("Enter the sql query : ")
        query(sql)
    else:
        break