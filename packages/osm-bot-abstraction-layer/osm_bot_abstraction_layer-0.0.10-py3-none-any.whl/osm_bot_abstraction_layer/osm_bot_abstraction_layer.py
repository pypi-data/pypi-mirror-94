# docs: http://osmapi.metaodi.ch/
import osmapi
import time
import json

def fully_automated_description():
    return "yes"

def manually_reviewed_description():
    return "no, it is a manually reviewed edit"

def get_api(account_type):
    with open('secret.json') as f:
        data = json.load(f)
        username = data[account_type]['username']
        password = data[account_type]['password']
        return osmapi.OsmApi(username = username, password = password)

def character_limit_of_description():
    return 255
 
class ChangesetBuilder:
    def __init__(self, affected_objects_description, comment, automatic_status, discussion_url, osm_wiki_documentation_page, source, other_tags_dict = {}):
        self.changeset_description = other_tags_dict
        self.changeset_description['automatic'] = automatic_status
        if automatic_status == fully_automated_description():
            if osm_wiki_documentation_page == None or discussion_url == None:
                raise "missing links to the automatic edit documentation!"
            self.changeset_description['bot'] = 'yes' # recommended on https://wiki.openstreetmap.org/wiki/Automated_Edits_code_of_conduct
            self.changeset_description["discussion_before_edits"] = discussion_url
            self.changeset_description["osm_wiki_documentation_page"] = osm_wiki_documentation_page
        self.changeset_description['created_by_library'] = "https://github.com/matkoniecz/osm_bot_abstraction_layer"
        self.changeset_description['cases_where_human_help_is_required'] = 'https://matkoniecz.github.io/OSM-wikipedia-tag-validator-reports/'
        if source != None:
            self.changeset_description["source"] = source
        self.changeset_description['comment'] = output_full_comment_get_comment_within_limit(affected_objects_description, comment)

    def create_changeset(self, api):
        print("opening changeset", json.dumps(self.changeset_description, sort_keys=True, indent=4))
        api.ChangesetCreate(self.changeset_description)

def get_data(id, type):
    print("downloading https://www.openstreetmap.org/" + type + "/" + str(id))
    api = get_api('bot_account')
    try:
        if type == 'node':
            return api.NodeGet(id)
        if type == 'way':
            return api.WayGet(id)
        if type == 'relation':
            return api.RelationGet(id)
    except osmapi.ElementDeletedApiError:
        return None
    assert(False)

def update_element(api, type, data):
    try:
        if type == 'node':
            return api.NodeUpdate(data)
        if type == 'way':
            return api.WayUpdate(data)
        if type == 'relation':
            return api.RelationUpdate(data)
        assert False, str(type) + " type as not recognised"
    except osmapi.ApiError as e:
        print(e)
        raise e

def delete_element(api, type, data):
    try:
        if type == 'node':
            return api.NodeDelete(data)
        if type == 'way':
            return api.WayDelete(data)
        if type == 'relation':
            return api.RelationDelete(data)
        assert False, str(type) + " type as not recognised"
    except osmapi.ApiError as e:
        print(e)
        raise e

def sleep(time_in_s):
    print("Sleeping")
    time.sleep(time_in_s)

def get_correct_api(automatic_status, discussion_url):
    if automatic_status == manually_reviewed_description():
        return get_api('human_account')
    elif automatic_status == fully_automated_description():
        assert(discussion_url != None)
        return get_api('bot_account')
    else:
        assert(False)

def output_full_comment_get_comment_within_limit(affected_objects_description, comment):
    full_comment = affected_objects_description + " " + comment
    if(len(comment) > character_limit_of_description()):
        raise "comment too long"
    if(len(full_comment) <= character_limit_of_description()):
        comment = full_comment
    print(full_comment)
    return comment

def make_edit(affected_objects_description, comment, automatic_status, discussion_url, osm_wiki_documentation_page, type, data, source, sleeping_time=60, other_tags_dict={}):
    api = get_correct_api(automatic_status, discussion_url)
    builder = ChangesetBuilder(affected_objects_description, comment, automatic_status, discussion_url, osm_wiki_documentation_page, source, other_tags_dict)
    builder.create_changeset(api)
    update_element(api, type, data)
    api.ChangesetClose()
    if sleeping_time != 0:
        sleep(sleeping_time)

def get_and_verify_data(osm_object_url, prerequisites, prerequisite_failure_callback=None):
    type = osm_object_url.split("/")[3]
    id = osm_object_url.split("/")[4]
    data = get_data(id, type)
    if data == None:
        return None
    failure = prerequisite_failure_reason(osm_object_url, prerequisites, data, prerequisite_failure_callback)
    if failure != None:
        print(failure)
        return None
    return data

def prerequisite_failure_reason(osm_object_url, prerequisites, data, prerequisite_failure_callback=None):
    if prerequisite_failure_callback != None:
        failure_reason = prerequisite_failure_callback(data)
        if failure_reason != None:
            return osm_object_url + " failed with " + failure_reason

    for key in prerequisites.keys():
        if prerequisites[key] == None:
            if key in data['tag']:
                return("failed " + key + " prerequisite, as key " + key + " was present for " + osm_object_url)
        elif key not in data['tag']:
            return("failed " + key + " prerequisite, as key " + key + " was missing for " + osm_object_url)
        elif prerequisites[key] != data['tag'][key]:
            return("failed " + key + " prerequisite for " + osm_object_url)
    return None
