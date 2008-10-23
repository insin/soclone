from soclone import badges
from soclone.models import Badge

badge_details = (
    (badges.AUTOBIOGRAPHER,     Badge.BRONZE, u'Autobiographer',     False, u'Completed all user profile fields'),
    (badges.CITIZEN_PATROL,     Badge.BRONZE, u'Citizen Patrol',     False, u'First flagged post'),
    (badges.CIVIC_DUTY,         Badge.SILVER, u'Civic Duty',         False, u'Voted 300 times'),
    (badges.CLEANUP,            Badge.BRONZE, u'Cleanup',            False, u'First rollback'),
    (badges.COMMENTATOR,        Badge.BRONZE, u'Commentator',        False, u'Left 10 comments'),
    (badges.CRITIC,             Badge.BRONZE, u'Critic',             False, u'First down vote'),
    (badges.DISCIPLINED,        Badge.BRONZE, u'Disciplined',        False, u'Deleted own post with 3 or more upvotes'),
    (badges.EDITOR,             Badge.BRONZE, u'Editor',             False, u'First edit'),
    (badges.ENLIGHTENED,        Badge.SILVER, u'Enlightened',        True,  u'First answer was accepted with at least ten up votes'),
    (badges.FAMOUS_QUESTION,    Badge.GOLD,   u'Famous Question',    True,  u'Asked a question with 10,000 views'),
    (badges.FAVOURITE_QUESTION, Badge.SILVER, u'Favourite Question', True,  u'Question favourited by 25 users'),
    (badges.GENERALIST,         Badge.SILVER, u'Generalist',         True,  u'Active in many different tags'),
    (badges.GOOD_ANSWER,        Badge.SILVER, u'Good Answer',        True,  u'Answer voted up more than 25 times'),
    (badges.GOOD_QUESTION,      Badge.SILVER, u'Good Question',      True,  u'Question voted up more than 25 times'),
    (badges.GREAT_ANSWER,       Badge.GOLD,   u'Great Answer',       True,  u'Answer voted up more than 100 times'),
    (badges.GREAT_QUESTION,     Badge.GOLD,   u'Great Question',     True,  u'Question voted up more than 100 times'),
    (badges.GURU,               Badge.SILVER, u'Guru',               True,  u'Judged best answer and voted up 40 times'),
    (badges.NECROMANCER,        Badge.BRONZE, u'Necromancer',        True,  u'Answered a question more than a year later with at least five up votes'),
    (badges.NICE_ANSWER,        Badge.BRONZE, u'Nice Answer',        True,  u'Answer voted up more than 10 times'),
    (badges.NICE_QUESTION,      Badge.BRONZE, u'Nice Question',      True,  u'Question voted up more than 10 times'),
    (badges.NOTABLE_QUESTION,   Badge.SILVER, u'Notable Question',   True,  u'Asked a question with 2,500 views'),
    (badges.ORGANISER,          Badge.BRONZE, u'Organiser',          False, u'First retag'),
    (badges.PEER_PRESSURE,      Badge.BRONZE, u'Peer Pressure',      False, u'Deleted own post with 3 or more downvotes'),
    (badges.POPULAR_QUESTION,   Badge.BRONZE, u'Popular Question',   True,  u'Asked a question with 1,000 views'),
    (badges.SCHOLAR,            Badge.BRONZE, u'Scholar',            False, u'First accepted answer'),
    (badges.SELF_LEARNER,       Badge.BRONZE, u'Self-Learner',       False, u'Answered your own question with at least 3 up votes'),
    (badges.SPECIALIST,         Badge.SILVER, u'Specialist',         True,  u'Highly active within a specific tag'),
    (badges.STELLAR_QUESTION,   Badge.SILVER, u'Stellar Question',   True,  u'Question favourited by 100 users'),
    (badges.STRUNK_AND_WHITE,   Badge.SILVER, u'Strunk & White',     False, u'Edited 100 entries'),
    (badges.STUDENT,            Badge.BRONZE, u'Student',            False, u'Asked first question with at least one up vote'),
    (badges.SUPPORTER,          Badge.BRONZE, u'Supporter',          False, u'First up vote'),
    (badges.TAXONOMIST,         Badge.SILVER, u'Taxonomist',         True,  u'Created a tag used by 50 questions'),
    (badges.TEACHER,            Badge.BRONZE, u'Teacher',            True,  u'Answered first question with at least one up vote'),
    (badges.YEARLING,           Badge.SILVER, u'Yearling',           False, u'Active member for a year'),
)

for id, type, name, multiple, description in badge_details:
    Badge.objects.create(id=id, type=type, name=name, description=description,
                         multiple=multiple)
