
#!Authentication


#? \\step 1\\:Register User\\ : user ka account create krna hoga => jisko we call as register User
#* is step mein hum user ki bhot saari details store karengein => 1.username , 2.password , email , name , mobile , address


#* password => hashed_password or encrypted_password => hum is tarah save krte encrypt kr ke
#* 123@123 => iska hashed version save hoga database mein


#? \\step 2:\\Login of the User\\  
'''
iske ander 3 steps hote hain: => then {} ye v steps hain jo 3rd ke ander hain 

1. validate User
2. validate password => if ye dono cheezein sahi hain then our backend => will generate Token
3. generate JWT token => hone ke baad => we will send this as {4}.[response Token] for frontend

then our frontend engineer responsible for storing that Response Token

because when we login => jwt token is stored => and then

suppose user login kr chuka hai => then login krne ke baad => mujhe validate krna hai means backend ko validate krna hai ki particular user kisi api ko access kr skta hai ya nhi kr skta hai

toh hum jab b koi next [api call - create task] karengein  => then hum particular api meim hum sath mein bhejengein is particular [response token] ko => {5}[apicall + response Token]

then jaise hi [api request] ayegi backend pr => first we will {6}.[VALIDATE] the token the response token

so , if token sahi hoga => access mil jayega => agar token sahi nhi hoga system kaheha we are [UNAUTHORIZED] \\ we are not allowed to access this api

'''

