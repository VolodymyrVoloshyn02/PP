from models import Session, Users, Banks, Credits, Transactions

session = Session()

user1 = Users(id = 1, name = 'Vova', passport = 'NK7555',address = 'Lviv,Geroiv UPA,45/17', phone_number='+3805475475457' , money_amount = 3442)
user2 = Users(id = 2, name = 'Anton', passport = 'PH455',address = 'Kyiv,Geroiv UPA,122/13', email = 'lol@gmail.com', phone_number='+380547777777' , money_amount = 9566)

bank1 = Banks(id = 1, all_money = 222200, per_cent = 10)
bank2 = Banks(id = 2, all_money = 35454, per_cent = 10)
bank3 = Banks(id = 3, all_money = 233440, per_cent = 10)

credits1 = Credits(id = 1,  start_date= '11-12-2020', end_date = '12-12-2021', start_sum = 1200, current_sum = 1349, bank_id = 1, user_id = 2 )
credits2 = Credits(id = 2,  start_date= '11-05-2019', end_date = '02-09-2021', start_sum = 15460, current_sum = 15649, bank_id = 2, user_id = 1 )
transaction = Transactions(id = 1, date = '23-06-2020', summ = 2000, credit_id = 1 )



session.add(user1)
session.add(user2)
session.add(bank1)
session.add(bank2)
session.add(bank3)
session.commit()
session.add(credits1)

session.add(credits2)
session.commit()

session.add(transaction)
session.commit()
session.close()