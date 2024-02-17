import sys
sys.path.append('/usr/local/lib/python3.9/site-packages/')
from flair.models import TextClassifier
from flair.data import Sentence

text = 'I love you so much, you are the best!'
text = '''A cohort of Twitter users with fake names and profile pictures have become a trusted source of information regarding drug cartel violence in Mexico.

These citizen journalists choose to remain anonymous to avoid violent backlash from gang members, but their reports have become increasingly influential.

On Jan. 8, a team from Microsoft Research published a paper called "The New War Correspondents: The Rise of Civic Media Curation in Urban Warfare," which details a social media study conducted over the past two years. Their main finding was that as Mexicans increasingly turn to Twitter for reports of violence, a core of mostly anonymous yet trusted curators have led the dissemination of public safety information.

"You find this small cluster of people, whom we call curators, who tend to be really well-regarded in their cities," Andrés Monroy-Hernández, one of the paper's five co-authors, tells Mashable. "These particular curators are those that have a lot of followers, which means that they're somewhat trusted by the community."

In the paper, the authors discuss how difficult it was to contact and interview the curators, who feel the work puts their lives in danger.

Those who did reply said that there was a feeling that Mexicans had been "abandoned by their government and the media." Mexico continues to show up on the Committee to Protect Journalists' list of most dangerous countries in the world for members of the media.

"Although traditional journalists regularly serve as curators, both on Twitter and in the more mainstream media outlets, the rise of citizen curators suggests that existing outlets are not meeting public need," the paper reads.

In fact, during the time of his research, Monroy-Hernández says he noticed the mainstream media even began to quote social media as a source in its own reporting:

"Social media has become a source of information for mainstream media, as well as a way for mainstream media to protect itself from retaliation from drug cartels."

Though these anonymous Twitter curators don't get paid for their work, it doesn't mean they are not dedicated. One told the researchers that spending up to 15 hours a day on Twitter is common.

According to Monroy-Hernández, his general sense is that these people provide this service for altruistic reasons.

Twitter user @BalaceraMTY has been reporting on violence in Monterrey for two years and has amassed more than 60,000 followers. In an email reply to Mashable, the owner of the account said the following:

"It all started on Twitter while I was looking for information on how to protect my relatives and myself, considering how violent the region had gotten at that point. It was vital to be properly informed of such dangerous circumstances. At the same time, I started commenting on the information I was gathering. I never thought my number of followers would grow the way it did. What do I get in return? Nothing economically, it’s not about that. It’s really just the satisfaction of being able to help, the idea of doing something so things can eventually get better."

The anonymous curator says they have been through extremely "hard times" in Monterrey over the past few years, but his or her belief is that things are getting better:

"While there is need to manage information, such as my time and health permits, I will continue trying to do my part."

Monroy-Hernández says this phenomenon is not specific to Mexico, and that Twitter has emerged as a trusted source of information in other places where violence occurs, particularly relating to organized crime.

For social media outlets to accomodate these reporters, the authors of the paper suggest that "there is a significant need for developing technical strategies to assess trust without revealing identity information."

The authors will formally present their findings at the Computer Supported Cooperative Work (CSCW 2013) conference in late February.'''
classifier = TextClassifier.load('en-sentiment')
s = Sentence(text)
classifier.predict(s)
total_sentiment = s.labels[0]
assert total_sentiment.value in ['POSITIVE', 'NEGATIVE']
sign = 1 if total_sentiment.value == 'POSITIVE' else -1
score = total_sentiment.score

print(sign * score)