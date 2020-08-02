#!/usr/bin/env python
import os
from production import Config

class devConfig(Config):
  NO_P_M_SPAM=True
  MAX_FLOOD_IN_P_M_s=99
  APP_ID = 1020699
  SHOW_HINDI="False"
  IG_LINK="https://instagram.com/r3d_._w0lf"
  GITHUB_LINK="https://github.com/authoritydmc"
  FB_LINK="https://fb.com/authoritydmc"
  SHOW_SOCIAL="True"
  APP_ID="1020699"
  API_HASH = "f79503413956b7daebe414d8c5a84fba"
  # DB_URI="postgres://beastbot:r3dw0lf@localhost:5432/beastbotdb"
  LYDIA_API="8952ba7638b05608697e357565a3a0cc3fac951cc55994f964dea32e04dc96b28eedd60afde3cd83aa0b8633de69f6dc3dcacc47079110622e79a15b26c646a3"
  DB_URI="postgres://rbawxavdvgxpys:97a6bc572f7842d7f3708c8d7f2dfc695c1f0ac757e41a8de3db667110ce68c2@ec2-54-235-207-226.compute-1.amazonaws.com:5432/d4b50o1s6h7hq3"

  HEROKU_API_KEY="skadkasaf"
  HEROKU_LINK="https://bot818283.herokuapps.com"
  HEROKU_APP_NAME=os.environ.get("HEROKU_APP_NAME",HEROKU_LINK.split(".")[0][8:] if  HEROKU_LINK!=None else "naa")
  

  SESSION="1BVtsOH0Bu4DA32L5qgixmTUg08tu5J7yIn2S1fNwkL9YSizzL4JBeTBSdWnJ-M0bsEtEuMohfkAzl-GfBrDxniCHGOYgJrp0XXQoindmjkAXrL6semHNYPxxQUhtM5vd93D6hb8LLbmLTv07Wos4kqS7Y8wqQI64wQGazzL_ZUMD6iB7eSeDitWGERs6klO0N7kUe5TEmySGwUuCflWG9DfR-wOm1OdP8V75f07sWfEBcQ_fcJJ9UkBZLAkvcMIHDjsj-G6C2w3qKWa6QmBjcKL5Mxfw1LfZD_UGfngRGzNR8do2PbxJLv36PHxHYFS_909BbhgGz8SVLAog2I2-JzWQ3XBwURg="


  
