This subfolder contains the class definitions for MQTT publisher and subscriber instances. \
The subscriber class can subscribe on a topic and receive messages, audio files, and audio transcriptions, all within the same method. \
The publisher class can send files and messages, with a separate member function for each. \
\
The only major roadblock we have currently is subscribing to multiple topics at once, which affects our capacity to send and receive audio messages.
