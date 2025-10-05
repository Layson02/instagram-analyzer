# Instagram Follower Analyzer

A command-line tool written in Python to analyze your Instagram data files (`followers_1.json` and `following.json`) and discover who doesn't follow you back.

## ✨ Features

* Calculates the total number of followers, following, and mutual connections.
* Identifies accounts that you follow but don't follow you back.
* Identifies accounts that follow you but you don't follow back.
* Displays a clean, formatted list of users who don't follow you back.
* Interactive and supports multiple languages (English and Portuguese).

## 📋 Prerequisites

To use this script, you first need to request your data from Instagram.

1.  On your Instagram profile, go to **Your activity > Download your information**.
2.  Request a download of your data in **JSON** format.
3.  Wait for the email from Instagram and download the `.zip` file.
4.  Inside the downloaded file, locate the following files:
    * `followers_and_following/followers_1.json`
    * `followers_and_following/following.json`

## 🚀 How to Use

1.  Make sure you have Python 3 installed.
2.  Clone or download this repository.
3.  Place the `followers_1.json` and `following.json` files in the same folder as the `analyzer.py` script (or in any subfolder). The script will find them automatically.
4.  Open a terminal and run the script:

```bash
python analyzer.py
```
5.  The program will first ask you to choose your preferred language (English or Portuguese).
6.  The analysis will be displayed in the terminal.

## 📝 Example Output

```
--- Instagram Analytics ---
Following                 : 520
Followers                 : 850
Mutual Followers          : 480
----------------------------
Don't Follow You Back     : 40
You Don't Follow Back     : 370

--- List of who doesn't follow you back (40) ---
example_user_1           example_user_2           example_user_3
example_user_4           example_user_5           example_user_6
...
```

## Acknowledgements

This project was inspired by and based on the original work of **[@ridwaanhall](https://github.com/ridwaanhall)**.