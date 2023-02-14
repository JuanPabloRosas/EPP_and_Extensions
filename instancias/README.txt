										Elaboration date : 19-07-2022

There are a total of 30 instances named as follows: stressPosition_instanceNum_precedenceNum. Example f_2_1
- 15 with stress at the beginning (i), that is, the stress level of the first 29 activities is between 0.4 and 0.5, 
  and the rest of the activities have a stress value between 0 and 0.2.
- 15 with stress at the end (f), that is, the stress level of the last 29 activities is between 0.4 and 0.5, 
  and the rest of the activities have a stress value between 0 and 0.2.
- 10 have no precedence constraints (_0)
- 10 have one precedence constraint (_1)
- 10 have two precedence constraints (_2)

The instances are made up of 10 columns:
Subject, Topic, Subtopic, Activity, Duration, Value, Stress, Requirement 1, Requirement 2, Mandatory.

Each instance has two subjects with two topics each. Each topic has two subtopics, 
and each subtopic has eleven activities, giving a total of 88 activities per instance.

- The duration of the activities is a random value between 3 and 15.
- The value of the activities is a random value between 9 and 15.
- The stress of the activities is a random value between 0 and 0.2 when the stress is normal, 
  and it is a random value between: 0.4 -0.5 when it is high stress.
- The column of requirement 1 and requirement 2 indicate which activities must be carried out before that activity
  and has a 0 in case it does not require any. You cannot have a requirement 2 without a requirement 1.
- The final column indicates which activities are mandatory, placing a 1 if the activity is mandatory 
  and a 0 otherwise.
