#!/usr/bin/env python
# coding: utf-8

# # LAB 8

# In[ ]:


import hashlib

possible_salt = ['overview', 'youve', 'been', 'asked', 'by', 'the', 'garda', 'to', 'assist', 'in', 'helping', 'retrieve', 'some', 
                 'hashed', 'passwords', 'they', 'have', 'managed', 'get', 'a', 'dump', 'of', 'one', 'database', 'tables', 'however', 'still',
                 'need', 'original', 'and', 'unable', 'crack', 'them', 'themselves', 'called', 'your', 'help', 'issue', 'seems', 'be', 'that',
                 'is', 'only', 'storing', 'password', 'hashes', 'so', 'far', 'their', 'attempts', 'brute', 'force', 'failed', 'tried', 
                 'standard', 'rainbow', 'without', 'success', 'suspect', 'may', 'salted', 'brief', 'analysis', 'supports', 'this', 'belief',
                 'indicates', 'all', 'same', 'salt', 'with', '2', 'lab', 'tasks', '2.1', 'task', '1', 'can', 'you', 'any', 'potentially', 'useful',
                 'information', 'from', 'case', 'files', 'policy', 'file', 'was', 'changed', 'in', '2010', 'created', 'after', 'this', 'date',
                 'are', 'alphanumeric', '5-7', 'characters', 'length', 'before', 'these', 'dates', 'believed', 'consisted', 'digits', 'its',
                 'used', 'value', 'somewhere', 'our', 'data', 'document', 'mysql', 'sites', 'domain', 'name', 'where', 'extracted', 'databse',
                 'www.exploringsecurity.com', 'no', 'need', 'visit', 'or', 'do', 'anything', 'on', 'actual', 'website', 'captured', 'javascript',
                 'code', 'site', 'reveals', 'format', 'as', 'commonhash', 'pass', 'much', 'below', 'for']

tomtom_pass = "06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2" # likely 5 - 7 digits

TARGET_HASHES = {
    "2834da08d58330d8dafbb2ac1c0f85f6b3b135ef",
    "92e54f10103a3c5111853c7098c04141f114719c1",
    "437fbc6892b38db6ac5bdbe2eab3f7bc924527d9",
    "fafa4483874ec051989d53e1e432ba3a6c6b9143",
    "06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2",
    "f44f3b09df53c1c11273def13cacd8922a86d48c"
}

def brute_force_salt():
    salt_found = "" # Empty string to store the salt
    for pass_ in range(9_999_999):
        for salt in possible_salt:
            # Pad to 7 digits with leading zeros
            seven_digits_padded = str(pass_).zfill(7)
            six_digits_padded = str(pass_).zfill(6)
            five_digits_padded = str(pass_).zfill(5)
            
            seven_d_likely_pass = hashlib.sha1((salt + seven_digits_padded).encode()).hexdigest()
            six_d_likely_pass = hashlib.sha1((salt + six_digits_padded).encode()).hexdigest()
            five_d_likely_pass = hashlib.sha1((salt + five_digits_padded).encode()).hexdigest()
            
            if tomtom_pass == seven_d_likely_pass:
                salt_found = salt
                break
            elif tomtom_pass == six_d_likely_pass:
                salt_found = salt
                break
            elif tomtom_pass == five_d_likely_pass:
                salt_found = salt
                break
        if salt_found != "":
            print(f"SALT FOUND!!! Salt: {salt} - Tomtom Password: {pass_}")
            break
    return salt_found

# output: SALT FOUND!!! Salt: www.exploringsecurity.com - Tomtom Password: 54321
salt = "www.exploringsecurity.com"
# uncomment this to brute force the salt (this will take a while)
# salt = brute_force_salt() 

# Trying dictionary attack - Using RockYou.txt as the dictionary to crack the hashes
with open("rockyou.txt", "r", encoding="utf-8", errors="ignore") as pw_file:
    print("Starting to crack passwords...")
    for line in pw_file:
        password = line.strip()
        hashed_password = hashlib.sha1((salt + password).encode()).hexdigest()
        if hashed_password in TARGET_HASHES:
            print(f"PASSWORD FOUND: {password} - hash: {hashed_password}")

# output: Starting to brute force passwords...
# PASSWORD FOUND: qwerty - hash: 437fbc6892b38db6ac5bdbe2eab3f7bc924527d9 (superman)
# PASSWORD FOUND: 54321 - hash: 06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2 (tomtom)
# PASSWORD FOUND: 121298 - hash: fafa4483874ec051989d53e1e432ba3a6c6b9143 (security)
# PASSWORD FOUND: Mark123 - hash: 92e54f10103a3c511853c7098c04141f114719c1 (Mark123)

'''
Trying brute force attack - Using all possible combinations of 5, 6, 7 characters
not feasible as it would take too long to complete - Decided to go for hashcat instead


num_found = 0
for length in range(5, 8):  # 5, 6, 7 characters
    for combo in itertools.product(string.ascii_letters + string.digits, repeat=length):
        password = ''.join(combo)
        hashed_password = hashlib.sha1((salt + password).encode()).hexdigest()
        if hashed_password in TARGET_HASHES:
            num_found += 1
            print(f"PASSWORD FOUND: {password} - hash: {hashed_password}")
            if num_found == len(TARGET_HASHES):
                print("All passwords found")
                break
'''



