# HOW TO RUN IT:
# 1. Open the .env file and input your email and password
#
# 2. Update your subscription preferences here:


import csv
import feedparser
from datetime import date
import LaTexAccents as TeX
from pylatexenc.latex2text import LatexNodes2Text
# import subprocess
# import base64
today = date.today()

converter = TeX.AccentConverter()

""" def latex_to_unicode(latex_string): # From https://tex.stackexchange.com/questions/274834/compile-latex-source-into-unicode-string
    '''Convert a LaTeX string to unicode.
    '''
    # Use pandoc for the job
    latex_string = base64.encodebytes(latex_string.encode())
    try:
        # This works in Python 3.4+
        return base64.b64decode(subprocess.check_output(
            ['pandoc', '-f', 'latex', '-t', 'plain'],
            input=latex_string)
            ).decode('utf-8')
    except TypeError:  # unexpected keyword 'input'
        p = subprocess.Popen(
            ['pandoc', '-f', 'latex', '-t', 'plain'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        stdout, _ = p.communicate(latex_string)
        stdout = base64.b64decode(stdout).decode('utf-8')
        return stdout.replace('\n', ' ').strip().decode('utf-8')
	
 """
def send_email(recipient_email,subscription_preferences,sender_email,sender_password):
	# Get a list of math subjects and math tags from 'subj-list.csv'
	with open('subj-list.csv','r') as f:
		reader = csv.reader(f)
		mathSubjects = list(reader)

	tag_dict = {xy[0] : xy[1] for xy in mathSubjects}

	# Generate HTML for the email
	html_top = """\
	<!DOCTYPE html>
	<html>
	<head>
		<style>
			#authors {
				text-align: center;
				font-style: italic;	
			}
			#subjectTitle{
				width:inherit;
				text-align:center;
			}
			#subject{
				text-align:center;
			}

			#tag, #xlistedtag, #updated{
				display: inline;
				color: white;
				border-radius: 8px;
				padding: 2px;
				font-size: 10px;
				margin: 2px;
				padding-left: 4px;
  				padding-right: 4px;
			}

			#tag{
				background-color: #984447;
			}
			#xlistedtag{
				background-color: #a65094;
			}

			#updated{
				background-color: #575757;
			}

			
@import url(https://fonts.googleapis.com/css?family=Merriweather:400,300,700);

@import url(https://fonts.googleapis.com/css?family=Montserrat:400,700);

body{
  background: #fbfbfb;
  font-family: 'Merriweather', serif;
  font-size: 16px;
  color:#777;
}
h1,h2,h4{
  font-family: 'Montserrat', sans-serif;
}
.row{
  padding:50px 0;
}
.separator{
  margin-bottom: 30px;
  width:100%;
  height:3px;
  background:#777;
  border:none;
  
}
.title{
  text-align: center;
  
  .row{
    padding: 50px 0 0;
  }
  
  h1{
    text-transform: uppercase;
  }
  
  .separator{
    margin: 0 auto 10px;
  }
}
.item {
  position: relative;
  margin-bottom: 30px;
  min-height: 1px;
  float: left;
  -webkit-backface-visibility: hidden;
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  
  .item-in {
    padding: 40px;
    position: relative;
  }
}
.item{
    
  h4{
      font-size: 18px;
      margin-top: 25px;
      letter-spacing: 2px;
      text-transform: uppercase;
    }
    p{
      font-size: 12px;
    }
    a{
      font-family: 'Montserrat', sans-serif;
	  font-size: inherit;
      text-transform: uppercase;
      color: #666666;
      margin-top: 10px;

      i {
        opacity: 0;
        padding-left: 0px;
        transition: 0.4s;
        font-size: 24px;
        display: inline-block;
        top: 5px;
        position: relative;
       }
      
      &:hover {
        text-decoration:none;
        i {
          padding-left: 10px;
          opacity: 1;
          font-weight: 300;
          }
        }
      }
    }
.item .icon {
  position:absolute;
  top: 27px;
  left: -16px;
  cursor:pointer;
    a{
      font-family: 'Merriweather', serif;
      font-size: 14px;
      font-weight:400;
      color: #999;
      text-transform:none;
    }
    svg{
      width:32px;
      height:32px;
      float:left;
    }
    .icon-topic{
      opacity: 0;
      padding-left: 0px;
      transition: 0.4s;
      display: inline-block;
      top: 0px;
      position: relative;
    }
    &:hover .icon-topic{
      opacity: 1;
      padding-left: 10px;
    }
  }
@media only screen and (max-width : 768px) {
  .item .icon{position: relative; top: 0; left:0;}
}

		</style>
		<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$']]
  }
};
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
	<link rel="stylesheet" href="https://matcha.mizu.sh/matcha.css">		
	</head>
	<body>
		<div id="body">
	"""
	text_top = "ArXiv Daily\n\n"

	html_bottom = """\
		</div>
	</body>
	</html>
	"""

	rss_html = ""
	rss_text = ""

	for subj in subscription_preferences:

		# Goes from math.AG -> Algebraic Geometry
		subj_title = tag_dict[subj]
		rss_url = "http://rss.arxiv.org/rss/" + str(subj)
		Feed = feedparser.parse(rss_url)
		pointer = Feed.entries

		rss_html += f"""\t<div id="subjectTitle">\t<h1 id="subjectTitleText"><a href="https://arxiv.org/list/{subj}/recent">{subj_title} [{subj}]</a></h1>\n\t</div>\n"""
		rss_html += """\t<div id="subject">\n"""

		for entry in pointer:

			# Get the title of the paper
			papertitle = str(entry.title)

			# Get the primary tag (note that entry.tags is a list)
			# The API convention, from what I can understand, lists the primary posting as the first tag
			primarytag = entry.tags[0].term


			# Make the list of tags, and the associated html
			tags_html = ''
			for x in entry.tags:
				tag = x.term
				if tag == primarytag:
					newtag = '<div id="tag">' + str(tag) + '</div>'
				else:
					newtag = '<div id="xlistedtag">' + str(tag) + '</div>'
				
				tags_html += newtag


			# Strip the entry.id at 'v' to get the version number
			# new entries by convention have v1
			version_number = entry.id.split('v')[2]

			version_html = ''
			if int(version_number) != 1:
				version_html += '<div id="updated">v' + str(version_number) + '</div>'



			# Get author info
			author_list = entry.author.split('\n')
			author_str = author_list[0]

			# If there are multiple authors
			if len(author_list) > 1:
				for i in range(1,len(author_list)):
					author_str = author_str + ', ' + author_list[i].lstrip()

			author_str = converter.decode_Tex_Accents(author_str, utf8_or_ascii=1)

			# Make the html for the entry
			entry_html = '\n\t\t<article><div class="col-md-6 item" id="paper">\n\t\t\t<div class="item-in">\n'

			# Add the link to the title
			entry_html += '<header><h4><a id="paperTitle" href="' + str(entry.link) + '">' + papertitle + '</a> '

			
			# Add tags and version info
			entry_html += tags_html + version_html

			entry_html += '</h4></header>'

			entry_html += '<div class="separator"></div>\n'

			# Add authors
			entry_html += '<br>\t<div id="authors">' + author_str + '</div>'

			# Add summary
			abstract = str(entry.summary).split('Abstract: ')[1]

			# Convert abstract via pylatexenc
			# abstract = LatexNodes2Text().latex_to_text(abstract)
			# abstract = latex_to_unicode(abstract)

			entry_html += '<br>\n\t\t' + abstract + '<br>\n'

			# entry_html = entry_html + '<a href="' + str(entry.link)+'"> Read More <i class="fa fa-long-arrow-right"></i></a>'

			entry_html += '</div></div></article>'

			# Add alternative text version of email
			entry_text = str(entry.title) + '\n\t' + author_str + '\n\n\t\t' + str(entry.summary)

			rss_html += entry_html
			rss_text += entry_text


		rss_html = rss_html + "\t</div>\n"


	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.image import MIMEImage


	msg = MIMEMultipart('alternative')
	msg['Subject'] = "ArXiv Daily - " + str(today.strftime("%B %d, %Y"))
	msg['From'] = sender_email
	msg['To'] = recipient_email

	# Create the body of the message (a plain-text and an HTML version).
	text = text_top + rss_text
	html = html_top + rss_html + html_bottom
	mail_html = html

	# print('HTML is :')
	# print(html)

	# ### Uncomment the following lines for testing:
	# testingpage = open('test.html','w')
	# testingpage.write(html)

	# Record the MIME types of both parts,text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(mail_html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	if sender_email is not None:
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login(sender_email, sender_password)
		mail.sendmail(sender_email, recipient_email, msg.as_string())
		mail.quit()
	return html

######################################################

# References:
#
# https://dev.to/maxhumber/how-to-send-and-schedule-emails-with-python-dnb
#
# https://stackoverflow.com/a/26369282
#
# 
