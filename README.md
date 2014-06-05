otp
===

Python script for one-time pad encryption and decryption. Kinda pointless, but I like it.

Purpose
-------
I created this script as part of a project in my Computer Forensics class. Our task was to create items in a file system which would be recovered by another team. I made this script to create an on-the-fly cipher for a file, and then output both the encrypted file and the one-time pad cipher (key file). For the project, I then also created 250 other randomly named key files, approximately half of them of the same size. I changed the timestamps on all but the correct key file, so that only the timestamp of the encrypted file and the correct key file would match. Recreating timelines is an important part of understanding digital forensic evidence, so the team should have been able to find it easily if they paid attention to that aspect of the files. Of course, there are also some other, less direct methods through which they could have discovered the correct file.

Inspiration
-----------
Having taken a Crypography class the prior semester, I was fascinated by the idea of the one-time pad, the one "unbreakable" form of cryto. Of course, it is not a very reasonable solution to normal cryptography problems, but I thought it would be fun to write a python script that would perform this form of crypto.
