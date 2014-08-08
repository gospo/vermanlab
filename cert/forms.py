# -*- coding: utf-8 -*-
from django import forms

class DeviceEnablementForm(forms.Form):
	# helper method for getRawAliasFromNamedTuple, returns a string of exactly 4 characters padded with 0
    def padAliasComponent(self, aliasComponentToPad):
        if aliasComponentToPad != 'null':
            aliasComponent = '0000'
            aliasComponent += aliasComponentToPad
            return aliasComponent[-4:]
        return "null"

    # method that takes an alias object from the DB and turns it into a colon-separated string
    def getRawAlias(self, alias):
        # only return as many alias compoennts as exist
        rawAlias = ""
        aliasComponent = self.padAliasComponent(alias['vendor'])
        if (aliasComponent != "null"):
            rawAlias += aliasComponent
        aliasComponent = self.padAliasComponent(alias['device'])
        if (aliasComponent != "null"):
            rawAlias += ":"
            rawAlias += aliasComponent
        aliasComponent = self.padAliasComponent(alias['subvendor'])
        if (aliasComponent != "null"):
            rawAlias += ":"
            rawAlias += aliasComponent
        aliasComponent = self.padAliasComponent(alias['subdevice'])
        if (aliasComponent != "null"):
            rawAlias += ":"
            rawAlias += aliasComponent
        return rawAlias

    def __init__(self,*args,**kwargs):
    	alias_list = kwargs.pop('alias_list')
    	pretty_aliases = []
    	for alias in alias_list:
    		pretty_aliases.append(self.getRawAlias(alias))
    	alias_tuples = zip(alias_list, pretty_aliases)
    	super(DeviceEnablementForm, self).__init__(*args,**kwargs)
        self.fields['selectedAlias'] = forms.ChoiceField(label="selectedAlias", choices=alias_tuples)