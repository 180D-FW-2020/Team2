from jiwer import wer

truth1_sphinx = ["i shall gunshot im finishing your surgical for the day in and in c. n. were being tailed its been a busy week lets catch up soon", 
				"wow michelle good job auditioning restriction goal for the day eliminated need to get moving to you it's been a busy week lets catch up soon", 
				"while michelle good job on finishing your striking gold for the day you know in a unique to get moving to you its been a busy week what had transpired",
				"while i shall good job on condition research in goal for the day you know in a need to get moving to help expand and is unique lets catch up soon",
				"ill ne'er shall good job i finish years searching go for the day you know and they need to get were going to or its been a busy week lets catch up soon",
				"well i shall good job on finish your stretching over the gate united they need to get moving to its been a busy week went to catch up soon",
				"shell good job on finishing years searching over the gate you any money to get willing to look its been a busy week let's catch up soon",
				"while michelle good job on initiator stretching over the gate you know in aiding me to get me into its been a busy week lets catch up soon",
				"while michelle good job on finishing your sturgeon over the gate you know it it needs to get more into it's been a busy week lets catch up soon",
				"well i shall good job on any shears sturgeon called reagan take you know it made me to get retail it's been busy me let's catch up soon"]

truth1_google = [ "bob michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "call michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "call michelle good job on finishing your stretching goal for the day he motivated me to get moving to its been a busy week lets catch up soon",
				  "call michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "wow michelle kujawa finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "wow michelle good job on finishing your stretching over the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "wild michelle job on finishing ear stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "well michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
				  "good job finishing your such and go for the day you motivated me to get moving to its been a busy week lets catch up soon"
				]

hyp1 = ["wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon",
			  "wow michelle good job on finishing your stretching goal for the day you motivated me to get moving to its been a busy week lets catch up soon"]


truth2_sphinx = ["hey isabelle when you did some guy didn't treat aids",
				 "isabel glad you did some guy in greeting",
				 "is it not glad you did some guy debriefing",
				 "hey isabelle glad you did some guy daydreaming",
				 "hey isabelle like you did some guy in treating",
				 "is it not glad you did some guy de breeding",
				 "hey isabelle crimes unit from guided breeding",
				 "he is about glad you did some guy inbreeding",
				 "hey isabelle why she gets indicted breeding",
				 "hey isabelle glad you did some guy inbreeding"
				]

truth2_google = ["hey Isabel glad you did some guided breathing",
				"hey Isabel glad you did some guided breathing",
				"hey Isabel glad you did some guided breathing",
				"hey Isabel glad you did some guided breathing",
				"Isabel glad you did some guided breathing",
				"Isabel glad you did some guided breathing",
				"hey Isabel glad you did some guided breathing",
				"hey Isabel glad you did some guided breathing",
				"hey Isabel glad you did some guided breathing",
				"Isabel glad you did some guided breathing"
				]

hyp2 = [	   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing",
			   "hey isabel glad you did some guided breathing"
				]

truth3_sphinx = ["aint jackie dont forget the jaguar today its been pretty drang valley really mature causes are going okay in your knowledge is feeding instant noodles",
				 "a jockey dont forget to drink water today its been pre jury how are you really look at classes are going okay youre not just the instant noodles",
				 "hang jackie dont forget to drink water today its been pretty drank how really older classes are going okay and youre not just being in stimulus",
				 "said jackie dont forget to drink water today its been creature and howry really put your glasses are going ok here in our just the instant noodles",
				 "said hey jack you don't forget to drink water today its in green giant howry maybe other classes are going on paying youre not just the instant noodles",
				 "came gently dont forget to drink water to make it in green giant our yuri me go to classes are going okay and youre not just he needs to be also",
				 "in fact he dont forget to drink water today is in green giant lapd again crosses are going okay in your knowledge is leaning in scandals",
				 "and jackie dont forget to drink water today its in green jacket how really the enterprises are going okay and youre not just the instant noodles",
				 "jackie dont forget to drug watergate a it's been pretty drank only read the other classes are going okay youre not just me and stimulus",
				 "a jacking dont forget to turn watergate this country dry now they may be under classes are going okay youre not just eating instant noodles"
				]

truth3_google = ["hey Jackie don't forget to drink water today has been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"Jackie don't forget to drink water today has been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"a jockey don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"hey Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"hey Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"hey Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"hey Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles",
				"hey Jackie don't forget to drink water today it's been pretty dry in La lately hope your classes are going okay and you're not just eating instant noodles"
		]

hyp3  = ["hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles",
				"hey jackie dont forget to drink water today its been pretty dry in LA lately hope your classes are going okay and youre not just eating instant noodles"
				]

truth4_sphinx = ["im michelle hope youre going on a box and call open on sundays and cakes and anti so cute",
				 "im michelle what youre going on locks and all out on some key knees and accent and he sent you",
				 "im michelle hope youre going to watch it on lal also can ease and accent hand he so cute",
				 "hello michelle appeared when one walks and apollo wilson can use and takes it in effect you",
				 "hello michelle oh dear god i walked to the hollow also denise and accent and he sent you",
				 "hello michelle were going on rocks at all ill also kidneys and takes it and hes so cute",
				 "hello michelle appeared on a box with apollo all sentries and takes it can be decent you",
				 "hello michelle what youre going on a box that follow on some tunis and takes it and he so cute",
				 "hello nourish our hope youre going on locks and all out on some kennys and exit and ease so cute",
				 "hello michelle and youre going on a box that hollow also denise and accent and easy so cute"
			]

truth4_google = ["hello Michelle hope you're going on walks and Apollo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks at the Palo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks with the Palo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks at the Palo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks with Apollo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks with Apollo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks with Apollo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks with Apollo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going on walks with Apollo also can you send pics of him he's so cute",
				 "hello Michelle hope you're going to walk so the Palo also can you send pics of him he's so cute"
]


hyp4 = [ "hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute",
				"hello michelle hope youre going on walks with apollo also can you send pics of him hes so cute"
				]

truth1_google = [each_string.lower().replace("'", "") for each_string in truth1_google]
truth2_google = [each_string.lower().replace("'", "") for each_string in truth2_google]
truth3_google = [each_string.lower().replace("'", "") for each_string in truth3_google]
truth4_google = [each_string.lower().replace("'", "") for each_string in truth4_google]

truth1_sphinx = [each_string.lower().replace("'", "") for each_string in truth1_sphinx]
truth2_sphinx = [each_string.lower().replace("'", "") for each_string in truth2_sphinx]
truth3_sphinx = [each_string.lower().replace("'", "") for each_string in truth3_sphinx]
truth4_sphinx = [each_string.lower().replace("'", "") for each_string in truth4_sphinx]

google_truth_list = [truth1_google, truth2_google, truth3_google, truth4_google]
sphinx_truth_list = [truth1_sphinx, truth2_sphinx, truth3_sphinx, truth4_sphinx]
hyp_list = [hyp1, hyp2, hyp3, hyp4]

print("GOOGLE RECOGNIZER")
for i in range(0,4):
	print("Word error rate for phrase",i+1,":",100*wer(google_truth_list[i], hyp_list[i]),"%")

print("SPHINX RECOGNIZER")
for i in range(0,4):
	print("Word error rate for phrase",i+1,":",100*wer(sphinx_truth_list[i], hyp_list[i]),"%")
