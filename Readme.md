# Arsys Dynamic DNS

A simple dynamic DNS script for [arsys](https://arsys.es) based domain names using their [DNS Hosting API](https://api.servidoresdns.net:54321/hosting/api/soap/index.php).

## Requirements

- python3
- pip
- zeep
- A registered domain name with arsys
- An API secret key (find it in your DNS zone control panel)

## Setup

### Config file

Enter your domain, the subdomain you want to change, the user, and the API secret into a `config.ini` file.

> **Note:** The `User` field is usually the name of your domain.

### Crontab configuration

We will set up crontab to run the script every minute in our linux server. Remember to use absolute paths when executing programs from crontab:

```
crontab -e
```

append the following line to the file:
```
* * * * * /usr/bin/python <this repo's path>/arsys_ddns.py
```

For example: 

```
* * * * * /usr/bin/python /home/guay/dev/arsys_ddns/arsys_ddns.py
```