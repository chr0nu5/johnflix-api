<p align="center">
  <img width="100%" src="_repo/logo.png">
</p>

# What this is

This is an opensource project, to study and try to organize media in a cool way. I`ve been using this for a while now, and decided to make it opensource so other people could use it to organize your personal stash of home-made movies and/or media. You can find the [frontend here](https://github.com/chr0nu5/johnflix-frontend).

# Where to start

This project was built using Docker, Python ♥️ and Django, so, it will work on your machine and on the server. I suggest you use AWS ECS to deploy this, to be easy and smooth. Before we start, we need a place to use as a storage. I am using `boto3` for that, so, S3 is the first choice for that. BUT, if you need an alternative, as good as S3, and cheaper, i would recommend [Backblaze](https://www.backblaze.com/). They are REALLY good.

# The basics

You should copy `.env.sample` to `.env` to start everything. This is the file:

```
PYTHONUNBUFFERED=1

POSTGRES_USER=api
POSTGRES_PASSWORD=n0td3f4u1t
POSTGRES_DB=api

DB_NAME=api
DB_USER=api
DB_PASSWORD=n0td3f4u1t
DB_HOST=db

SECRET_KEY=3m*rww8--^9!y7x&!j4pj4!v3oa@uc^d%t3__t4v^q!h1n
DEBUG=True

# AWS or BackBlaze Key/Sec
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# AWS or BackBlaze Bucket/Url
S3_BUCKET=
S3_BUCKET_URL=

FRONTEND_URL=

CACHE_TTL=3600

CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

Attention to AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET, S3_BUCKET_URL. This is all for storage. You need to know what you are doing. There is `NO LOCAL STORAGE`. The `FRONTEND_URL` should be provided so some links on the `admin` interface works well to validate some models and information. This is the URL where you deployed the [frontend](https://github.com/chr0nu5/johnflix-frontend).

The `CSRF_TRUSTED_ORIGINS` is a new security feature on django, just provice the API url here.

# Build

After the `.env` is set, just run

```
docker compose build api
```

# Folder structure

Just to highlight some special folders. Also, there is a cool `import` feature for the project, be ready :) 

`/app/tmp` here is where all the upload (and some magic) happens. Be kind with it.

`/app/convert` this is where all the files for conversion should be.

`/app/import` this is where all the files ready for import should be.

`/app/_patch` i was not able to overcome a django secyrity feature, so i had to do a litthe patch on the file, to bypass some validation for file operations.

# Admin

The admin has all the features you need to register your home-made movies. Lemme explain a few models here (/app/content/models.py).

`Genre` and `Tag` are for categorizing your movies.

`Content` this is the main category of the files. They will build the menu of the website, after movies. This are not movies, this is everything you can organize in chapters (or seasons) with a list of episodes.

`Media` is a content, like, a tv show, or an anime. Everymedia should be related to a `Content`

`Season` every season is releated to a `Media`

`Subtitle` are for subtitle files, in `vtt` format -> [read here](https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API).

`Episode` self-explainable. An episode for a season, for a media, for a content.

`Movie` this is for movies, wow. Some fiels are auto-populated if you use the importer. Do not (or avoid) use the admin to upload the files.

`Playlist` let`s you create a list of movies.

# MAGIC

(we use (ffmpeg)[https://ffmpeg.org/] for the magic)

Now the magic starts. I decided to automate a lof of things to make it easier for people who have a lot of files. So, a lot of management commands (django, thank you) are available to do the `import` task. Let`s go over all the commands. Just to remember, this is how you run a command in django. Assuming you are using docker, you can do:

```
docker compose exec api bash
./manage.py command_name
```

## Command: ./manage.py converter

This one is going to look in `/app/convert` folder, and start a few tasks, all the finished files are sent to `/app/import` to be imported.

1 - If you put video files not in MP4 (or m4v) format, for example `mkv`, it will convert the file to a `.mp4` using the h264 codec. The problem here is that the browser can't play mkv, avi or other `strange` formats. So, a good format is `.mp4` with `h264`. The converted files will have only 1 audio track, it will search for `eng` or `por` in the metadata info.

2 - If you have `.srt` files, it can convert the files to `.vtt` for html5 video support.

## Command: ./manage.py importer

This is the BEAST. It will do the heavy work for you, with a few steps to make it work. It can import `movies`, `episodes` and `photos` (yes, there is a photo feature, but you have to discover for yourself). For a `movie`, imagine that you have `bigbuckbunny.mp4` in `/app/import/bigbuckbunny.mp4`. We need to provide a file to the `importer` so the job starts. 

# Cover files and images

All the images should be in jpg, jpeg or png format. I use pillow under the hood but there`s no support for webm, for example. You can open a PR :)

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
