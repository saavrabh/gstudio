from django.http import HttpResponseRedirect
#from django.http import HttpResponse
from django.shortcuts import render_to_response #render  uncomment when to use
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django_mongokit import get_database
from django.contrib.auth.models import User

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

from gnowsys_ndf.settings import GAPPS, MEDIA_ROOT
from gnowsys_ndf.ndf.models import GSystemType, Node 
from gnowsys_ndf.ndf.views.methods import get_node_common_fields
collection = get_database()[Node.collection_name]


def task(request, group_name, task_id=None):
    """
    * Renders a list of all 'task' available within the database.
    """
    ins_objectid  = ObjectId()
    if ins_objectid.is_valid(group_name) is False :
      group_ins = collection.Node.find_one({'_type': "Group","name": group_name})
      auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
      if group_ins:
        group_id = str(group_ins._id)
      else :
        auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
        if auth :
          group_id = str(auth._id)
    else :
        pass

    GST_TASK = collection.Node.one({'_type': "GSystemType", 'name': 'Task'})
    title = "Task"
    TASK_inst = collection.GSystem.find({'member_of': {'$all': [GST_TASK._id]}, 'group_set': {'$all': [ObjectId(group_id)]}})
    template = "ndf/task.html"
    variable = RequestContext(request, {'title': title, 'TASK_inst': TASK_inst, 'group_id': group_id, 'groupid': group_id, 'group_name':group_name })
    return render_to_response(template, variable)

def task_details(request, group_name, task_id):
    """
    * Renders a 'task' details.
    """
    ins_objectid  = ObjectId()
    if ins_objectid.is_valid(group_name) is False :
      group_ins = collection.Node.find_one({'_type': "Group","name": group_name})
      auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
      if group_ins:
        group_id = str(group_ins._id)
      else :
        auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
        if auth :	
          group_id = str(auth._id)
    else :
        pass
    task_node = collection.Node.one({'_type': u'GSystem', '_id': ObjectId(task_id)})
    at_list = ["Status", "start_time", "Priority", "end_time", "Assignee", "Estimated_time"]
    blank_dict = {}
    history = []
    subtask = []
    for each in at_list:
	attributetype_key = collection.Node.find_one({"_type":'AttributeType', 'name':each})
        attr = collection.Node.find_one({"_type":"GAttribute", "subject":task_node._id, "attribute_type.$id":attributetype_key._id})
        if attr:
		blank_dict[each] = attr.object_value
    if task_node.prior_node :
	blank_dict['parent'] = collection.Node.one({'_id':task_node.prior_node[0]}).name 
    if task_node.post_node :
	for each_postnode in task_node.post_node:
		sys_each_postnode = collection.Node.find_one({'_id':each_postnode})
		sys_each_postnode_user = User.objects.get(id=sys_each_postnode.created_by)
		member_of_name = collection.Node.find_one({'_id':sys_each_postnode.member_of[0]}).name 
		if member_of_name == "Task" :
			subtask.append({'id':str(sys_each_postnode._id), 'name':sys_each_postnode.name, 'created_by':sys_each_postnode_user.username, 'created_at':sys_each_postnode.created_at})
		if member_of_name == "task_update_history":
			history.append({'id':str(sys_each_postnode._id), 'name':sys_each_postnode.name, 'created_by':sys_each_postnode_user.username, 'created_at':sys_each_postnode.created_at, 'altnames':eval(sys_each_postnode.altnames), 'content':sys_each_postnode.content})
    history.reverse()
    var = { 'title': task_node.name,'group_id': group_id, 'groupid': group_id, 'group_name': group_name, 'node':task_node, 'history':history, 'subtask':subtask}
    var.update(blank_dict)
    variables = RequestContext(request, var)
    template = "ndf/task_details.html"
    return render_to_response(template, variables)

@login_required
def create_edit_task(request, group_name, task_id=None):
    """Creates/Modifies details about the given Task.
    """
    edit_task_node = ""
    change_list = []
    parent_task_check = ""
    ins_objectid  = ObjectId()
    if ins_objectid.is_valid(group_name) is False :
        group_ins = collection.Node.find_one({'_type': "Group","name": group_name})
        auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
        if group_ins:
            group_id = str(group_ins._id)
        else :
            auth = collection.Node.one({'_type': 'Author', 'name': unicode(request.user.username) })
            if auth :
                group_id = str(auth._id)
    else :
        pass
    blank_dict = {}
    if task_id:
        task_node = collection.Node.one({'_type': u'GSystem', '_id': ObjectId(task_id)})
	edit_task_node = task_node
	at_list = ["Status", "start_time", "Priority", "end_time", "Assignee", "Estimated_time"]
    	
    	for each in at_list:
		attributetype_key = collection.Node.find_one({"_type":'AttributeType', 'name':each})
        	attr = collection.Node.find_one({"_type":"GAttribute", "subject":task_node._id, "attribute_type.$id":attributetype_key._id})
        	if attr:
			blank_dict[each] = attr.object_value
	if task_node.prior_node :
		pri_node = collection.Node.one({'_id':task_node.prior_node[0]})
		blank_dict['parent'] = pri_node.name 
		blank_dict['parent_id'] = str(pri_node._id)
    else:
        task_node = collection.GSystem()


    var = { 'title': 'Task','group_id': group_id, 'groupid': group_id, 'group_name': group_name, 'node':edit_task_node, 'task_id':task_id }
    var.update(blank_dict)
    context_variables = var
    if request.method == "POST": # create or edit
        name = request.POST.get("name","")
        content_org = request.POST.get("content_org","")
        parent = request.POST.get("parent","")
        Status = request.POST.get("Status","")
        Start_date = request.POST.get("Start_date","")
        Priority = request.POST.get("Priority","")
        Due_date = request.POST.get("Due_date","")
        Assignee = request.POST.get("Assignee","")
        Estimated_time = request.POST.get("Estimated_time","")
        GST_TASK = collection.Node.one({'_type': "GSystemType", 'name': 'Task'})
	if not task_id: # create
        	get_node_common_fields(request, task_node, group_id, GST_TASK)
	if parent: # prior node saving
		if not task_id:		
			task_node.prior_node = [ObjectId(parent)]
			parent_object = collection.Node.find_one({'_id':ObjectId(parent)})
			parent_object.post_node = [task_node._id]
			parent_object.save()
		else : #update
			if not task_node.prior_node == [ObjectId(parent)] :
				parent_task_check = "yes"
				if not task_node.prior_node :
					task_node.prior_node = [ObjectId(parent)]
					changed_object = collection.Node.find_one({'_id':ObjectId(parent)})
					changed_object.post_node.append(task_node._id)
					changed_object.save()
					change_list.append('parent set to '+changed_object.name.encode('utf8'))
				else :
					parent_object = collection.Node.find_one({'_id':task_node.prior_node[0]})
					parent_object.post_node.remove(task_node._id)
					parent_object.save()
					task_node.prior_node = [ObjectId(parent)]
					changed_object = collection.Node.find_one({'_id':ObjectId(parent)})
					changed_object.post_node.append(task_node._id)
					changed_object.save()
					change_list.append('Parent changed from '+parent_object.name.encode('utf8')+' to '+changed_object.name.encode('utf8')) # updated details

        task_node.save()
	at_list = ["Status", "start_time", "Priority", "end_time", "Assignee", "Estimated_time"] # fields
	if not task_id: # create
	    for each in at_list:
	         if request.POST.get(each,""):
			attributetype_key = collection.Node.find_one({"_type":'AttributeType', 'name':each})
               		newattribute = collection.GAttribute()
                	newattribute.subject = task_node._id
                	newattribute.attribute_type = attributetype_key
                	newattribute.object_value = request.POST.get(each,"")
                	newattribute.save()
	else: #update
	    for each in at_list:
		if request.POST.get(each,""):
			attributetype_key = collection.Node.find_one({"_type":'AttributeType', 'name':each})
        		attr = collection.Node.find_one({"_type":"GAttribute", "subject":task_node._id, "attribute_type.$id":attributetype_key._id})
			if attr : # already attribute exist 
				if not attr.object_value == request.POST.get(each,"") :	
					change_list.append(each.encode('utf8')+' changed from '+attr.object_value.encode('utf8')+' to '+request.POST.get(each,"").encode('utf8')) # updated details	  
					attr.object_value = request.POST.get(each,"")
					attr.save()
					
					
			else :
				attributetype_key = collection.Node.find_one({"_type":'AttributeType', 'name':each})
               			newattribute = collection.GAttribute()
                		newattribute.subject = task_node._id
                		newattribute.attribute_type = attributetype_key
                		newattribute.object_value = request.POST.get(each,"")
                		newattribute.save()
				change_list.append(each.encode('utf8')+' set to '+request.POST.get(each,"").encode('utf8')) # updated details
	    if change_list or content_org :
		GST_task_update_history = collection.Node.one({'_type': "GSystemType", 'name': 'task_update_history'})
	        update_node = collection.GSystem()
		get_node_common_fields(request, update_node, group_id, GST_task_update_history)
		if change_list :
			update_node.altnames = unicode(str(change_list))
		update_node.prior_node = [task_node._id]		
		update_node.save()
		update_node.name = unicode(task_node.name.encode('utf8')+"-update_history-"+str(update_node._id))
		update_node.save()
		task_node.post_node.append(update_node._id)
		task_node.save()			

        return HttpResponseRedirect(reverse('task_details', kwargs={'group_name': group_name, 'task_id': str(task_node._id) }))

    return render_to_response("ndf/task_create_edit.html",
                                  context_variables,
                                  context_instance=RequestContext(request)
                              )

