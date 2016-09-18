# -*- coding: utf-8 -*-
sql_selectall = """insurance_nullfix.claim.HOSP_CODE,
  insurance_nullfix.cust.AGE,
  insurance_nullfix.cntt.CNTT_YM
  """
sql_selectall_list=sql_selectall.split(',')
print sql_selectall_list
for i in range(0,len(sql_selectall_list)):
  pop_column=sql_selectall_list.pop(i)
  col_select=','.join(sql_selectall_list) #하나 빼서 쿼리 내용물 만들고
  sql_selectall_list.insert(i,pop_column) #바로 다시 되돌려둔다. 
  sql_cuclaim="""Select """+col_select+""" From
  insurance_nullfix.claim Left Join
  insurance_nullfix.cust
    On insurance_nullfix.claim.CUST_ID = insurance_nullfix.cust.CUST_ID
  Left Join
  insurance_nullfix.cntt
    On insurance_nullfix.claim.POLY_NO = insurance_nullfix.cntt.POLY_NO And
    insurance_nullfix.cntt.CUST_ID = insurance_nullfix.claim.CUST_ID
  where
  cust.SIU_CUST_YN = """
  print sql_cuclaim,'\n'
