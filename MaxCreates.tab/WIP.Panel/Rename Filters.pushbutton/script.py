# -*- coding: utf-8 -*-
__title__ = "Rename\nFilters"
__doc__ = """Version = 1.0
Date    = 28.10.2024
_____________________________________________________________________
Description:
Rename Views in Revit by using Find/Replace Logic
_____________________________________________________________________
How-to:
-> Click on the button
-> Select Views
-> Define Renaming Rules
-> Rename Views
_____________________________________________________________________
Last update:
- [28.10.2024] - 1.1 First Release
_____________________________________________________________________
Author: Máximo Cubero"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================

from Autodesk.Revit.DB import ElementId, LabelUtils, BuiltInParameter

def get_parameter_name_by_id(doc, param_id):
    """
    Get the name of a parameter by its ID.

    Args:
        doc: The current Revit document.
        param_id (ElementId or int): The parameter ID as an ElementId or an integer.

    Returns:
        str: The name of the parameter, or None if not found.
    """
    # Ensure param_id is an ElementId
    if not isinstance(param_id, ElementId):
        param_id = ElementId(param_id)

    # Check if it's a built-in parameter
    try:
        built_in_param = BuiltInParameter(param_id.IntegerValue)
        if built_in_param != BuiltInParameter.INVALID:
            return LabelUtils.GetLabelFor(built_in_param)
    except:
        pass

    # Check if it's a shared parameter
    shared_param = doc.GetElement(param_id)
    if shared_param:
        return shared_param.Name

    return None


    # Check if it's a shared parameter
    shared_param = doc.GetElement(element_id)
    if shared_param:
        return shared_param.Name

    return None

# param_id = -1002053  # Workset parameter ID
# param_name = get_parameter_name_by_id(doc, param_id)
#
# if param_name:
#     print("Parameter Name: {}".format(param_name))
# else:
#     print("Parameter ID {} not found.".format(param_id))

def get_workset_by_id(doc, workset_id):
    """
    Get a workset by its ID.

    Args:
        doc: The current Revit document.
        workset_id (int): The ID of the workset to retrieve.

    Returns:
        Workset: The workset object if found, otherwise None.
    """
    workset_table = doc.GetWorksetTable()
    workset = workset_table.GetWorkset(WorksetId(workset_id))
    return workset

def get_filter_type_text(filter_obj):
    """
    Get the string representation of a Revit filter type.

    Args:
        filter_obj: The filter object (e.g., FilterStringEquals, FilterNumericEquals, etc.).

    Returns:
        A string that represents the filter type (e.g., 'Equals', 'Contains', etc.).
    """
    if isinstance(filter_obj, FilterIntegerRule):
        return 'Integer'
    elif isinstance(filter_obj, FilterInverseRule):
        return 'Not'

    elif isinstance(filter_obj, FilterNumericEquals):
        return 'Equals'
    elif isinstance(filter_obj, FilterNumericGreater):
        return 'Is Greater Than'
    elif isinstance(filter_obj, FilterNumericGreaterOrEqual):
        return 'Is Greater Than Or Equal To'
    elif isinstance(filter_obj, FilterNumericLess):
        return 'Is Less Than'
    elif isinstance(filter_obj, FilterNumericLessOrEqual):
        return 'Is Less Than Or Equal To'
    elif isinstance(filter_obj, FilterNumericRuleEvaluator):
        return 'Numeric Rule'
    elif isinstance(filter_obj, FilterNumericValueRule):
        return 'Numeric Value'

    elif isinstance(filter_obj, FilterStringBeginsWith):
        return 'Begins With'
    elif isinstance(filter_obj, FilterStringContains):
        return 'Contains'
    elif isinstance(filter_obj, FilterStringEndsWith):
        return 'Ends With'
    elif isinstance(filter_obj, FilterStringEquals):
        return 'Equals'
    elif isinstance(filter_obj, FilterStringGreater):
        return 'Is Greater Than'
    elif isinstance(filter_obj, FilterStringGreaterOrEqual):
        return 'Is Greater Than Or Equal To'
    elif isinstance(filter_obj, FilterStringLess):
        return 'Is Less Than'
    elif isinstance(filter_obj, FilterStringLessOrEqual):
        return 'Is Less Than Or Equal To'
    elif isinstance(filter_obj, FilterStringRuleEvaluator):
        return 'String Rule'

    elif isinstance(filter_obj, FilterValueRule):
        return 'Value Rule'



    # Add more cases as needed for other filter types
    else:
        return 'Unknown Filter Type'

def get_all_parameters_names_and_ids(doc):
    """
    Get the names and IDs of all parameters in the document.

    Args:
        doc: The current Revit document.

    Returns:
        A dictionary where the key is the parameter's ID and the value is the parameter's name.
    """
    parameter_info = {}

    # Collect all elements in the document
    collector1 = FilteredElementCollector(doc).WhereElementIsNotElementType()  # Instances
    collector2 = FilteredElementCollector(doc).WhereElementIsElementType()  # Types

    collector = list(collector1) + list(collector2)

    # Iterate through all elements
    for element in collector:
        # Loop through all parameters of the element
        for param in element.Parameters:
            # Check if the parameter's Definition is not None before accessing its Name
            if param.Definition:
                parameter_info[param.Id] = param.Definition.Name  # Add to dictionary

    return parameter_info


def get_filter_rule(doc, rule, parameter_id):

    rule_filter = "TBC"
    rule_value = "TBC"

    if isinstance(rule, FilterIntegerRule):
        rule_filter = get_filter_type_text(rule.GetEvaluator())
        rule_value = rule.RuleValue
        #print('Integer Rule')
    elif isinstance(rule, FilterStringRule):
        rule_filter = get_filter_type_text(rule.GetEvaluator())
        rule_value = rule.RuleString
        #print ('String Rule')
    elif isinstance(rule, FilterDoubleRule):
        rule_filter = get_filter_type_text(rule.GetEvaluator())
        rule_value = rule.RuleValue
        #print('Double Rule')
    elif isinstance(rule, FilterInverseRule):
        rule_filter_inverse_rule = get_filter_rule(doc, rule.GetInnerRule(), parameter_id)
        rule_filter = rule_filter_inverse_rule[0]
        rule_value_id = rule_filter_inverse_rule[1]
        rule_value = get_workset_by_id(doc, rule_value_id).Name
        #print('Inverse Rule')
    elif isinstance(rule, FilterElementIdRule):
        if rule.UsesLevelFiltering(doc, parameter_id):
            rule_filter = 'Level'
        else:
            rule_filter = 'Element Id'
        rule_value = doc.GetElement(rule.RuleValue).Name
        #print('Element Id Rule')
    elif isinstance(rule, HasValueFilterRule):
        rule_filter = 'Has Value'
        rule_value = 'Empty'
        #print('Has Value Rule')
    elif isinstance(rule, HasNoValueFilterRule):
        rule_filter = 'Has No Value'
        rule_value = 'Empty'
        #print('Has No Value Rule')
    else:
        pass
        #print('Other Rule')

    return (rule_filter, rule_value)

""" Rename views on sheets
    SHEET NUMBER + DETAIL NUMBER + TITLE ON SHEET (IF POPULATED)
    SHEET NUMBER + DETAIL NUMBER + VIEW NAME
"""

#def rule_condition:


# forms.alert("WIP-Rename Filters")

all_filter        = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()

project_parameters = get_all_parameters_names_and_ids(doc)

aux = []

for filter in all_filter:

    filter_name = filter.Name
    print('FILTER NAME: {}'.format(filter_name))

    get_categories_id = filter.GetCategories()
    categories = [Category.GetCategory(doc, category_id).Name for category_id in get_categories_id]
    print('CATEGORIES SELECTED: {}'.format(categories))

    print('CONDITIONS/RULES:')
    # get_element_filters = filter.GetElementFilter().GetFilters()

    try:
        get_element_filters = filter.GetElementFilter().GetFilters()
    except:
        rule = 'No Rules'
        print(rule)
        print("-" * 100)
        continue

    for enum, f in enumerate(get_element_filters, 1):
        rules = f.GetRules()
        for rule in rules:
            print('#' * 50)
            rule_number = 'Rule ' + str(enum) + ':'
            print(rule_number)

            # PARAMETER NAME
            rule_parameter_id = rule.GetRuleParameter()
            print(type(rule_parameter_id))
            try:    rule_parameter = get_parameter_name_by_id(doc, rule_parameter_id)
            #try:    rule_parameter = project_parameters[rule_parameter_id]
            except: rule_parameter = "It couldn't get the parameter name. Check!"



            print('Rules: {}'.format(type(rule)))
            get_filter_rule(doc, rule, rule_parameter_id)
            #print('Rule Type: {}'.format(get_filter_type_text(rule)))

            aux.append(type(rule))

            # RULE FILTER
            rule_filter = get_filter_rule(doc,rule, rule_parameter_id)[0]
            rule_value = get_filter_rule(doc,rule, rule_parameter_id)[1]

            # # RULE CONDITION
            # try:
            #     rule_condition = rule.GetEvaluator()
            #     rule_condition_name = get_filter_type_text(rule_condition)
            # except: rule_condition_name = 'Not found'
            #
            # if hasattr(rule, "GetEvaluator"):
            #     try:
            #         rule_value = rule.RuleString
            #     except: rule_value = 'check!'
            # elif hasattr(rule, "GetInnerRule"):
            #     try:
            #         rule_value = rule_condition.RuleValue
            #     except: rule_value = 'check!'
            # else:
            #     rule_condition_name = 'To be defined'
            #     rule_value = 'To be defined'

            rule_summary =  ('Parameter: ID: {}, NAME: {}\n'
                            'Rule Filter: {}\n'
                            'Rule Value: {}'
                            .format(rule_parameter_id,rule_parameter, rule_filter, rule_value))
        print(rule_summary)

    print("-" * 100)


output = set(aux)
for i in output:
    print(i)


from Autodesk.Revit.DB import ElementId, LabelUtils, BuiltInParameter




# e_id = ElementId(-1002053)
# print (doc.GetElement(e_id))
