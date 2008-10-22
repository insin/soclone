import re

from django import forms

tagname_re = re.compile(r'^[-a-z0-9+#.]+$')
tag_split_re = re.compile(r'[ ;,]')

class TagnameField(forms.CharField):
    """
    A CharField which validates that a maximum of 5 space-separated
    tagnames have been entered, that each tag is at most 25
    characters long and that no duplicate tagnames were entered.
    """
    def clean(self, value):
        value = super(TagnameField, self).clean(value)
        if value == u'':
            return value
        tagnames = [name for name in tag_split_re.split(value) if name]
        if len(tagnames) > 5:
            raise forms.ValidationError(u'You may only enter up to 5 tags.')
        for tagname in tagnames:
            if len(tagname) > 24:
                raise forms.ValidationError(u'Each tag may be no more than 24 '
                                            u'characters long.')
            if not tagname_re.match(tagname):
                raise forms.ValidationError(u'Tags may only include the '
                                            u'following characters: '
                                            u'[a-z 0-9 + # - .]')
        if len(tagnames) != len(set(tagnames)):
            raise forms.ValidationError(u'The same tag was entered multiple '
                                        u'times.')
        return u' '.join(tagnames)
