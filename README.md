<p align="center">
  <img width="100%" src="_repo/logo.png">
</p>

# What this is

This is an opensource project, to study and try to organize media in a cool way. I`ve been using this for a while now, and decided to make it opensource so other people could use it to organize your personal stash of home-made movies and/or media. You can find the [frontend here](https://github.com/chr0nu5/johnflix-frontend).

# Where to start

This project was built using Docker, Python ♥️ and Django, so, it will work on your machine and on the server. I suggest you use AWS ECS to deploy this, to be easy and smooth. Before we start, we need a place to use as a storage. I am using `boto3` for that, so, S3 is the first choice for that. BUT, if you need an alternative, as good as S3, and cheaper, i would recommend [Back Blaze](https://www.backblaze.com/). They are REALLY good.

# Licence

```
Good Use Disclaimer License

This open-source project is provided under the Good Use Disclaimer License.
By accessing, cloning, or using any part of this project, you agree to
abide by the terms outlined in this license.

1. Good Use Requirement:
   You are permitted to use this project only for purposes that align with
   the principles of ethical behavior, respect for human rights, and
   promotion of societal well-being. Good use encompasses activities that
   contribute positively to society, foster collaboration, and adhere to
   legal and ethical standards.

2. No Responsibility for Misuse:
   The creator(s) of this project expressly disclaim any responsibility
   for its use in activities that are harmful, unethical, illegal, or 
   otherwise detrimental to individuals, communities, or society at 
   large. The user assumes full responsibility for ensuring that their 
   use of this project complies with applicable laws, regulations, and 
   ethical norms.

3. Limitation of Liability:
   In no event shall the creator(s) of this project be liable for any 
   damages, including without limitation, direct, indirect, incidental, 
   special, consequential, or punitive damages, arising out of the use 
   of or inability to use this project, regardless of the cause of 
   action or the theory of liability, even if advised of the possibility 
   of such damages.

4. No Endorsement:
   The presence of this project does not imply any endorsement or 
   affiliation with individuals, organizations, products, or services. 
   Any references to specific entities are purely for informational 
   purposes and do not constitute endorsements.

5. No Warranty:
   This project is provided on an "as is" basis, without warranties of 
   any kind, express or implied. The creator(s) of this project make no 
   representations or warranties regarding the accuracy, completeness, 
   or reliability of the information contained herein.

6. Acceptance:
   By accessing, cloning, or using any part of this project, you 
   acknowledge that you have read, understood, and agree to be bound 
   by the terms of this license.

7. Modification:
   The creator(s) of this project reserve the right to modify or update 
   this license at any time without prior notice. It is your 
   responsibility to review this license periodically for changes.

If you do not agree with these terms,
you are not permitted to access or use this project.
```
