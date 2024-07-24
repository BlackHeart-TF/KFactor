otpauth-migration://offline?data=ChsKBXglKzojEgxwYXNzd29yZDhkaWcgASgCMAIKKQoFeCUrOiMSEmlzc3VlcjpwYXNzd29yZDYwcxoGaXNzdWVyIAEoATACEAEYASAAKImBn%2BoE
{'proto': 'otpauth-migration', 'url': 'offline', 'query': {'data': 'ChsKBXglKzojEgxwYXNzd29yZDhkaWcgASgCMAIKKQoFeCUrOiMSEmlzc3VlcjpwYXNzd29yZDYwcxoGaXNzdWVyIAEoATACEAEYASAAKImBn+oE'}}
ChsKBXglKzojEgxwYXNzd29yZDhkaWcgASgCMAIKKQoFeCUrOiMSEmlzc3VlcjpwYXNzd29yZDYwcxoGaXNzdWVyIAEoATACEAEYASAAKImBn+oE
0a 1b 0a 05 78 25 2b 3a 23 12 0c 70 61 73 73 77 6f 72 64 38 64 69 67 20 01 28 02 30 02 0a 29 0a 05 78 25 2b 3a 23 12 12 69 73 73 75 65 72 3a 70 61 73 73 77 6f 72 64 36 30 73 1a 06 69 73 73 75 65 72 20 01 28 01 30 02 10 01 18 01 20 00 28 89 81 9f ea 04 
0a 10 .  //magic number?
1b 27 .  
0a 10 .   //secret tag
05 5 .    //secret len
78 120 x   //decoded secret
25 37 %
2b 43 +
3a 58 :
23 35 #
12 18 .    //accoutn tag
0c 12 .    //account length
70 112 p
61 97 a
73 115 s
73 115 s
77 119 w
6f 111 o
72 114 r
64 100 d
38 56 8
64 100 d
69 105 i
67 103 g
20 32        //algorithm tag
01 1 .       //algorithm value: SHA1
28 40 (      // tag, digits?
02 2 .       // is this 8?
30 48 0      // otp type tag
02 2 .       // typ type value: totp
0a 10 .
29 41 )
0a 10 .
05 5 .
78 120 x
25 37 %
2b 43 +
3a 58 :
23 35 #
12 18 .
12 18 .
69 105 i
73 115 s
73 115 s
75 117 u
65 101 e
72 114 r
3a 58 :
70 112 p
61 97 a
73 115 s
73 115 s
77 119 w
6f 111 o
72 114 r
64 100 d
36 54 6
30 48 0
73 115 s
1a 26 .
06 6 .
69 105 i
73 115 s
73 115 s
75 117 u
65 101 e
72 114 r
20 32  
01 1 .
28 40 (
01 1 .
30 48 0
02 2 .
10 16 .
01 1 .
18 24 .
01 1 .
20 32  
00 0 .
28 40 (
89 137 .
81 129 .
9f 159 .
ea 234 .
04 4 .