#test account shit

import Account_Management

Account_Management.init_subscribe('+1747629273')
Account_Management.init_subscribe('+124')
Account_Management.send_problem('+1747629273','learn spanish')
Account_Management.send_problem('+124','learn math')
print Account_Management.recieve_answer('+1747629273','el pan')
print Account_Management.recieve_answer('+124','9')
print Account_Management.check_points('+1747629273')
print Account_Management.check_points('+124')
print Account_Management.del_subscribe('+124')