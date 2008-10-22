from soclone.models import Badge

badge_details = (
    (1, Badge.BRONZE, u'Autobiographer', u'Completed all user profile fields', False),
    (2, Badge.SILVER, u'Beta', u'Actively participated in the SOClone private beta', False),
    (3, Badge.BRONZE, u'Citizen Patrol', u'First flagged post', False),
    (4, Badge.SILVER, u'Civic Duty', u'Voted 300 times', False),
    (5, Badge.BRONZE, u'Cleanup', u'First rollback', False),
    (6, Badge.BRONZE, u'Commentator', u'Left 10 comments', False),
    (7, Badge.BRONZE, u'Critic', u'First down vote', False),
    (8, Badge.BRONZE, u'Editor', u'First edit', False),
    (9, Badge.SILVER, u'Enlightened', u'First answer was accepted with at least ten up votes', True),
    (10, Badge.GOLD, u'Famous Question', u'Asked a question with 10,000 views', True),
    (11, Badge.SILVER, u'Generalist', u'Active in many different tags', True),
    (12, Badge.SILVER, u'Good Answer', u'Answer voted up more than 25 times', True),
    (13, Badge.SILVER, u'Good Question', u'Question voted up more than 25 times', True),
    (14, Badge.GOLD, u'Great Answer', u'Answer voted up more than 100 times', True),
    (15, Badge.GOLD, u'Great Question', u'Question voted up more than 100 times', True),
    (16, Badge.SILVER, u'Guru', u'Judged best answer and voted up 40 times', True),
    (17, Badge.BRONZE, u'Necromancer', u'Answered a question more than a year later with at least five up votes', True),
    (18, Badge.BRONZE, u'Nice Answer', u'Answer voted up more than 10 times', True),
    (19, Badge.BRONZE, u'Nice Question', u'Question voted up more than 10 times', True),
    (20, Badge.SILVER, u'Notable Question', u'Asked a question with 2,500 views', True),
    (21, Badge.BRONZE, u'Organizer', u'First retag', False),
    (22, Badge.BRONZE, u'Popular Question', u'Asked a question with 1,000 views', True),
    (23, Badge.BRONZE, u'Scholar', u'First accepted answer', False),
    (24, Badge.BRONZE, u'Self-Learner', u'Answered your own question with at least 3 up votes', False),
    (25, Badge.SILVER, u'Specialist', u'Highly active within a specific tag', True),
    (26, Badge.SILVER, u'Strunk & White', u'Edited 100 entries', False),
    (27, Badge.BRONZE, u'Student', u'Asked first question with at least one up vote', False),
    (28, Badge.BRONZE, u'Supporter', u'First up vote', False),
    (29, Badge.SILVER, u'Taxonomist', u'Created a tag used by 50 questions', True),
    (30, Badge.BRONZE, u'Teacher', u'Answered first question with at least one up vote', True),
    (31, BBadge.SILVER, u'Yearling', u'Active member for a year', False),
)

for id, type, name, description, multiple in badge_details:
    Badge.objects.create(id=id, type=type, name=name, description=description,
                         multiple=multiple)
